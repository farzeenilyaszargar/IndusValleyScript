"""Seeded structural experiments using Python's standard library only."""
import collections as C
import hashlib
import json
import math
import random
import statistics as S
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'

def save(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2) + '\n')

def entropy(counts):
    total = sum(counts.values())
    return -sum(n / total * math.log2(n / total) for n in counts.values()) if total else 0

def describe(texts):
    uni = C.Counter(s for t in texts for s in t)
    bi = C.Counter((a, b) for t in texts for a, b in zip(t, t[1:]))
    prev = C.Counter()
    for (a, b), n in bi.items():
        prev[a] += n
    h = -sum(n / sum(bi.values()) * math.log2(n / prev[a]) for (a, b), n in bi.items()) if bi else 0
    repeats = {}
    for k in range(2, 7):
        phrases = C.Counter(p for t in texts for p in set(tuple(t[i:i+k]) for i in range(len(t)-k+1)))
        repeats[str(k)] = sum(n >= 2 for n in phrases.values())
    return {'texts': len(texts), 'tokens': sum(uni.values()), 'signs': len(uni),
            'mean_length': S.mean(map(len, texts)), 'median_length': S.median(map(len, texts)),
            'max_length': max(map(len, texts)), 'unigram_entropy_bits': entropy(uni),
            'conditional_entropy_bits': h, 'hapax_fraction': sum(n == 1 for n in uni.values()) / len(uni),
            'top10_token_fraction': sum(n for _, n in uni.most_common(10))/sum(uni.values()),
            'repeated_subsequences_in_distinct_texts': repeats}

def conditional_entropy(texts):
    bi = C.Counter((a, b) for t in texts for a, b in zip(t, t[1:]))
    total = sum(bi.values())
    prev = C.Counter()
    for (a, b), n in bi.items():
        prev[a] += n
    return -sum(n / total * math.log2(n / prev[a]) for (a, b), n in bi.items()) if total else 0

def shuffled(texts, kind, rng):
    result = [list(t) for t in texts]
    if kind == 'within_text':
        for t in result:
            rng.shuffle(t)
    elif kind == 'global_frequency':
        flat = [s for t in result for s in t]
        rng.shuffle(flat)
        start = 0
        for i, t in enumerate(result):
            result[i] = flat[start:start+len(t)]
            start += len(t)
    elif kind == 'length_position':
        groups = C.defaultdict(list)
        for i, t in enumerate(result):
            groups[len(t)].append(i)
        for length, indices in groups.items():
            for j in range(length):
                column = [result[i][j] for i in indices]
                rng.shuffle(column)
                for i, value in zip(indices, column):
                    result[i][j] = value
    else:
        raise ValueError(kind)
    return result

def nulls(texts, trials=199):
    observed = conditional_entropy(texts)
    out = {'observed_bits': observed, 'trials': trials, 'tail': 'lower', 'seed': 20261015}
    for kind in ['within_text', 'global_frequency', 'length_position']:
        rng = random.Random(20261015)
        values = [conditional_entropy(shuffled(texts, kind, rng)) for _ in range(trials)]
        out[kind] = {'mean': S.mean(values), 'sd': S.stdev(values), 'min': min(values), 'max': max(values),
                     'p_monte_carlo': (1 + sum(v <= observed for v in values))/(trials+1),
                     'values': values}
    out['interpretation'] = 'Rejecting shuffles supports structure under this null; it does not identify language or meaning.'
    return out

def canonical(t):
    return min(tuple(t), tuple(reversed(t)))

def split(texts, seed):
    groups = C.defaultdict(list)
    for t in texts:
        groups[canonical(t)].append(tuple(t))
    keys = sorted(groups)
    random.Random(seed).shuffle(keys)
    a, b = int(.8*len(keys)), int(.9*len(keys))
    return [[t for key in ks for t in groups[key]] for ks in (keys[:a], keys[a:b], keys[b:])]

class Model:
    def __init__(self, train, order=2, strength=5):
        self.order, self.strength = order, strength
        self.vocab = sorted({s for t in train for s in t} | {'<UNK>', '<EOS>'})
        self.uni, self.context = C.Counter(), [None, C.defaultdict(C.Counter), C.defaultdict(C.Counter)]
        for t in train:
            prefix = ['<BOS>', '<BOS>']
            for s in list(t)+['<EOS>']:
                self.uni[s] += 1
                self.context[1][tuple(prefix[-1:])][s] += 1
                self.context[2][tuple(prefix[-2:])][s] += 1
                prefix.append(s)
        self.total = sum(self.uni.values())
        self.totals = [None]+[{ctx: sum(c.values()) for ctx, c in contexts.items()}
                             for contexts in self.context[1:]]

    def prob(self, s, prefix):
        s = s if s in self.uni else '<UNK>'
        prefix = [x if x in self.uni or x == '<BOS>' else '<UNK>' for x in prefix]
        p = (self.uni[s]+.5)/(self.total+.5*len(self.vocab))
        for k in range(1, self.order):
            ctx = tuple(prefix[-k:])
            counts = self.context[k].get(ctx, {})
            n = self.totals[k].get(ctx, 0)
            p = (counts.get(s, 0)+self.strength*p)/(n+self.strength)
        return p

    def losses(self, texts):
        values = []
        for t in texts:
            prefix = ['<BOS>', '<BOS>']
            loss = 0
            for s in list(t)+['<EOS>']:
                loss -= math.log2(self.prob(s, prefix))
                prefix.append(s)
            values.append((loss, len(t)+1))
        return values

def avg_loss(values):
    return sum(x for x, _ in values)/sum(n for _, n in values)

def evaluate(texts, seed):
    train, val, test = split(texts, seed)
    result = {'seed': seed, 'train': len(train), 'validation': len(val), 'test': len(test),
              'split_policy': 'exact and reversed copies grouped; 80/10/10 groups; fixed seed',
              'test_groups': [list(canonical(t)) for t in test]}
    models, losses = {}, {}
    for order in (1, 2, 3):
        candidates = [(strength, Model(train, order, strength)) for strength in (1, 5, 20, 100)]
        strength, model = min(candidates, key=lambda x: avg_loss(x[1].losses(val)))
        values = model.losses(test)
        result[f'order_{order}'] = {'strength': strength, 'validation_bits': avg_loss(model.losses(val)),
                                  'test_bits_per_token_including_EOS': avg_loss(values),
                                  'perplexity': 2**avg_loss(values)}
        models[order], losses[order] = model, values
    delta = [(a[0]-b[0], a[1]) for a, b in zip(losses[1], losses[2])]
    rng = random.Random(seed)
    boots = sorted(avg_loss(rng.choices(delta, k=len(delta))) for _ in range(500))
    result['bigram_improvement_bits'] = avg_loss(delta)
    result['bigram_improvement_bootstrap95'] = [boots[12], boots[487]]
    known = set(models[2].uni)
    result['unknown_test_tokens'] = sum(s not in known for t in test for s in t)
    result['test_sign_tokens'] = sum(map(len, test))
    # Mask every test sign, using two visible neighbours only; no target leakage.
    scores = C.Counter()
    model = models[2]
    candidates = [s for s in model.vocab if s not in ('<EOS>', '<UNK>')]
    majority = max(candidates, key=lambda s: (model.uni[s], s))
    for t in test:
        for i, target in enumerate(t):
            left = '<BOS>' if i == 0 else t[i-1]
            right = '<EOS>' if i == len(t)-1 else t[i+1]
            rank = sorted(candidates, key=lambda s: (-model.prob(s, [left])*model.prob(right, [s]), s))
            scores['total'] += 1
            scores['top1'] += target == rank[0]
            scores['top5'] += target in rank[:5]
            scores['unigram_top1'] += target == majority
    result['mask_prediction'] = dict(scores) | {f'{k}_rate': scores[k]/scores['total']
                                               for k in ('top1', 'top5', 'unigram_top1')}
    return result

def embeddings_and_grammar(texts):
    train, val, test = split(texts, 42)
    counts = C.Counter(s for t in train for s in t)
    positions = C.defaultdict(C.Counter)
    contexts = C.defaultdict(C.Counter)
    for t in train:
        for i, s in enumerate(t):
            role = 'singleton' if len(t)==1 else 'initial' if i==0 else 'final' if i==len(t)-1 else 'medial'
            positions[s][role] += 1
            contexts[s]['L:'+(t[i-1] if i else '<BOS>')] += 1
            contexts[s]['R:'+(t[i+1] if i<len(t)-1 else '<EOS>')] += 1
    totals = C.Counter()
    for cs in contexts.values():
        totals.update(cs)
    grand = sum(totals.values())
    sparse, vectors = {}, {}
    for sign, cs in sorted(contexts.items()):
        row_total = sum(cs.values())
        sparse[sign] = {c: max(0, math.log2(n*grand/(row_total*totals[c]))) for c, n in cs.items()}
        v = [0.0]*32
        for context, weight in sparse[sign].items():
            digest = hashlib.sha256(context.encode()).digest()
            for i in range(32):
                v[i] += weight*(1 if digest[i] & 1 else -1)/math.sqrt(32)
        norm = math.sqrt(sum(x*x for x in v)) or 1
        vectors[sign] = [x/norm for x in v]
    save('embeddings_sparse_ppmi.json', sparse)
    save('embeddings_32d.json', {'method': 'signed SHA256 random projection of directional PPMI; unit normalization',
                                'training_only': True, 'dimension': 32, 'vectors': vectors})
    norms = {s: math.sqrt(sum(x*x for x in v.values())) for s, v in sparse.items()}
    neighbours = {}
    for s in sorted(counts, key=lambda s: (-counts[s], s))[:40]:
        sims = []
        for other in sparse:
            if other == s or counts[other]<5:
                continue
            dot = sum(w*sparse[other].get(c,0) for c,w in sparse[s].items())
            sim = dot/(norms[s]*norms[other]) if norms[s]*norms[other] else 0
            sims.append((sim,other))
        neighbours[s] = [{'sign': o, 'cosine': x} for x,o in sorted(sims, reverse=True)[:5]]
    save('context_neighbours.json', neighbours)
    # Position labels are operational roles, not parts of speech.
    roles = {}
    for sign,n in counts.items():
        role,k = positions[sign].most_common(1)[0]
        roles[sign] = role if n>=10 and k/n>=.65 else 'flexible' if n>=10 else 'rare'
    patterns = C.Counter(tuple(roles[s] for s in t) for t in train)
    held = [tuple(roles.get(s,'unseen') for s in t) for t in test]
    coverage = sum(p in patterns for p in held)/len(held)
    rng = random.Random(42)
    shuffled_held = [tuple(roles.get(s,'unseen') for s in t) for t in shuffled(test,'within_text',rng)]
    save('grammar.json', {'method': 'training-only positional classes and empirical finite template grammar',
                         'thresholds': {'min_count':10,'dominant_position_fraction':.65},
                         'roles': roles, 'role_counts': dict(C.Counter(roles.values())),
                         'templates': [{'roles':list(p),'train_count':n} for p,n in patterns.most_common()],
                         'test_texts':len(test), 'test_exact_template_coverage':coverage,
                         'shuffled_test_template_coverage':sum(p in patterns for p in shuffled_held)/len(held),
                         'limitation':'No semantic or phonetic interpretation; rare/flexible classes are broad.'})
    save('position_profiles.json', {s: {'count': counts[s], 'positions': dict(positions[s]), 'role':roles[s]}
                                    for s in sorted(counts)})

def numeral_fish(cisi):
    catalog = json.loads((ROOT/'data/processed/parpola_catalog.json').read_text())
    fish = {r['id'] for r in catalog if 48 <= int(r['id'][1:]) <= 65}
    # Catalogue range containing simple stroke groups; inspect descriptions in the ledger.
    # Do not include complex signs merely because their description mentions strokes.
    tally = {f'P{i:03}' for i in list(range(121,131))+[144,145,147,150,151]}
    texts = [r['signs'] for r in cisi]
    def count(ts):
        bi = C.Counter((a,b) for t in ts for a,b in zip(t,t[1:]))
        return sum(n for (a,b),n in bi.items() if a in tally and b in fish)
    actual = count(texts)
    rng = random.Random(42)
    values = [count(shuffled(texts,'within_text',rng)) for _ in range(499)]
    save('numeral_fish.json', {'corpus':'clean deduplicated CISI, read right-to-left',
        'fish_ids': sorted(fish), 'tally_like_ids':sorted(tally), 'observed_tally_then_fish':actual,
        'trials':len(values), 'null_mean':S.mean(values),
        'p_upper':(1+sum(v>=actual for v in values))/(1+len(values)),
        'scope':'Descriptions provide morphology only. Stroke count is not assigned a numerical value.',
        'limitation':'Small selected Mohenjo-daro subset; enrichment cannot distinguish stars, goods, names, or quantities.'})

def main():
    OUT.mkdir(exist_ok=True)
    records = json.loads((ROOT/'data/processed/icit_unique.json').read_text())
    texts = [r['signs'] for r in records]
    cisi = json.loads((ROOT/'data/processed/cisi_unique.json').read_text())
    save('descriptive.json', {'ICIT':describe(texts),'CISI':describe([r['signs'] for r in cisi])})
    save('entropy_nulls.json', nulls(texts))
    save('sequence_models.json', [evaluate(texts,seed) for seed in (42,43,44,45,46)])
    save('reverse_models.json', evaluate([list(reversed(t)) for t in texts],42))
    embeddings_and_grammar(texts)
    numeral_fish(cisi)
    # Hold out every sequence also attested in the target site (duplicates remain in raw metadata).
    allrows = json.loads((ROOT/'data/processed/icit_all.json').read_text())
    site_results = {}
    for site in ('Harappa','Mohenjo-daro'):
        target = {tuple(r['signs']) for r in allrows if not r['exclusion_reasons'] and r['site']==site}
        target_keys = {canonical(t) for t in target}
        train = [t for t in texts if canonical(t) not in target_keys]
        if train and target:
            site_results[site] = {'train':len(train),'test':len(target),
                'unigram_bits':avg_loss(Model(train,1,20).losses(sorted(target))),
                'bigram_bits':avg_loss(Model(train,2,20).losses(sorted(target))),
                'strength':20,'selection':'fixed, no target-site tuning'}
    save('site_transfer.json', site_results)
    print(json.dumps({'descriptive':describe(texts), 'site_transfer':site_results},indent=2))

if __name__ == '__main__':
    main()
