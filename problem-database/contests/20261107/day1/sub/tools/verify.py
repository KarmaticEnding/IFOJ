#!/usr/bin/env python3
"""Verify the segment-tree solution before any official data is generated."""
from pathlib import Path
import hashlib, itertools, json, random, subprocess, tempfile, time

ROOT = Path(__file__).resolve().parents[1]
P = 993244853

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def brute(a, operations):
    a = a[:]
    answers = []
    for op in operations:
        t, l, r = op[:3]
        if t == 1:
            for i in range(l - 1, r):
                a[i] = (a[i] + op[3]) % P
        else:
            # Explicitly enumerate subarrays, independent of the weighted-sum formula.
            total = 0
            for i in range(l - 1, r):
                s = 0
                for j in range(i, r):
                    s += a[j]
                    total += s
            answers.append(total % P)
    return answers

def encode(a, ops):
    return ('%d %d\n' % (len(a), len(ops)) + ' '.join(map(str, a)) + '\n' +
            ''.join(' '.join(map(str, op)) + '\n' for op in ops)).encode()

def main():
    started = time.time()
    build = ROOT / 'tools' / '.build'
    build.mkdir(exist_ok=True)
    std, ref, ubsan = [build / x for x in ('sub', 'reference', 'sub-ubsan')]
    for source, binary, flags in [
        (ROOT/'GPT/sub.cpp', std, ['-O2', '-DLOCAL']),
        (ROOT/'tools/reference.cpp', ref, ['-O2']),
        (ROOT/'GPT/sub.cpp', ubsan, ['-O1', '-DLOCAL', '-fsanitize=undefined,bounds', '-fno-sanitize-recover=all'])
    ]:
        subprocess.run(['g++', '-std=c++14', '-Wall', '-Wextra', *flags, str(source), '-o', str(binary)], check=True)
    def run(binary, text):
        result = subprocess.run([str(binary)], input=text, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=15, check=True)
        assert not result.stderr, result.stderr.decode()
        return list(map(int, result.stdout.split()))
    count = 0
    def check(a, ops, sanitize=False):
        nonlocal count
        text = encode(a, ops)
        expected = brute(a, ops)
        assert run(std, text) == expected, ('segment tree mismatch', a, ops)
        assert run(ref, text) == expected, ('Fenwick mismatch', a, ops)
        if sanitize:
            assert run(ubsan, text) == expected
        count += 1
    # Exhaustive initial arrays and every possible query/update interval, including n=1.
    for n in range(1, 6):
        intervals = [(l, r) for l in range(1, n+1) for r in range(l, n+1)]
        for a in itertools.product((1, P-1), repeat=n):
            ops = [(2, l, r) for l, r in intervals]
            for l, r in intervals:
                ops.extend([(1, l, r, P-1), (2, 1, n), (2, l, r), (1, l, r, 1)])
            check(list(a), ops, sanitize=True)
    rng = random.Random(20261107)
    for case in range(1000):
        n = rng.randint(1, 35 if case < 900 else 120)
        a = [rng.choice([1, P-1, P-2, rng.randrange(1, P)]) for _ in range(n)]
        ops = []
        for i in range(rng.randint(1, 150)):
            l, r = sorted((rng.randint(1,n), rng.randint(1,n)))
            if i % 13 == 0: l, r = 1, n
            if i % 17 == 0: r = l
            if rng.randrange(2):
                ops.append((1,l,r,rng.choice([1,P-1,P-2,rng.randrange(1,P)])))
            else:
                ops.append((2,l,r))
        check(a, ops, sanitize=case < 80)
    # Check the actual submission's mandatory sub.in/sub.out behavior as well.
    file_binary = build / 'sub-file'
    subprocess.run(['g++','-std=c++14','-O2',str(ROOT/'GPT/sub.cpp'),'-o',str(file_binary)],check=True)
    a, ops = [P-1,1,P-1], [(2,1,3),(1,1,3,P-1),(2,2,2),(2,1,3)]
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder)
        (path/'sub.in').write_bytes(encode(a,ops))
        subprocess.run([str(file_binary)],cwd=folder,check=True,timeout=5)
        assert list(map(int,(path/'sub.out').read_text().split())) == brute(a,ops)
    report = {'verified_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
              'standard_sha256': digest(ROOT/'GPT/sub.cpp'),
              'reference_sha256': digest(ROOT/'tools/reference.cpp'),
              'brute_force_cases': count, 'sanitizer_cases': 142,
              'file_io_checked': True, 'elapsed_seconds': round(time.time()-started,3)}
    (ROOT/'tools/verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)

if __name__ == '__main__':
    main()
