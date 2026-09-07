"""Phase 5 perf probe: time every live API endpoint (bypasses proxy)."""
import json
import time
import urllib.request

BASE = 'http://127.0.0.1:8898'
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def post(path, payload, timeout=300):
    t0 = time.perf_counter()
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json'})
    with _opener.open(req, timeout=timeout) as r:
        body = json.loads(r.read())
    return (time.perf_counter() - t0) * 1000, body


def get(path):
    t0 = time.perf_counter()
    with _opener.open(BASE + path, timeout=60) as r:
        body = r.read()
    return (time.perf_counter() - t0) * 1000, len(body)


if __name__ == '__main__':
    ms, _ = get('/api/health')
    print(f"health: {ms:.0f}ms")
    ms, _ = get('/api/meta')
    print(f"meta: {ms:.0f}ms")
    ms, b = post('/api/episode', {'family': 'linear', 'strategy': 'state',
                                  'seed': 7, 'n_demos': 4})
    print(f"episode: {ms:.0f}ms correct={b.get('correct')}")
    ms, b = post('/api/compare', {'family': 'linear', 'seed': 7,
                                  'n_demos': 4,
                                  'strategies': ['state', 'context',
                                                 'frozen']})
    print(f"compare3: {ms:.0f}ms")
    ms, b = post('/api/interference', {'family': 'linear', 'seed_a': 1,
                                       'seed_b': 2, 'strategy': 'state'})
    print(f"interference: {ms:.0f}ms")
    ms, b = post('/api/intervene', {'family': 'linear', 'seed': 7,
                                    'strategy': 'state'})
    print(f"intervene: {ms:.0f}ms")
    ms, b = post('/api/sweep', {'family': 'linear', 'strategy': 'state',
                                'axis': 'n_demos', 'points': [1, 4, 8],
                                'n_tasks': 25, 'seed_base': 0})
    print(f"sweep(3pts x 25tasks, flagship N_D): {ms:.0f}ms "
          f"n={len(b.get('points', []))}")
    ms, _ = get('/api/precomputed?exp=001_task_acquisition_linear')
    print(f"precomputed: {ms:.0f}ms")
    ms, _ = get('/api/figure?name=fig1_acquisition.png')
    print(f"figure: {ms:.0f}ms")
