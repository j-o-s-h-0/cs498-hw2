import time, uuid, requests

A = "http://34.121.1.7:8080"
B = "http://35.205.179.169:8080"

def latency_test(base, name):
    reg = []
    lst = []

    for _ in range(10):
        u = "u" + uuid.uuid4().hex[:8]
        t0 = time.time()
        requests.post(base + "/register", json={"username": u})
        reg.append((time.time() - t0) * 1000)

    for _ in range(10):
        t0 = time.time()
        requests.get(base + "/list")
        lst.append((time.time() - t0) * 1000)

    print(name)
    print("/register avg ms:", round(sum(reg) / len(reg), 2))
    print("/list avg ms:", round(sum(lst) / len(lst), 2))
    print()

def consistency_test(iters):
    misses = 0
    for _ in range(iters):
        u = "u" + uuid.uuid4().hex[:8]
        requests.post(A + "/register", json={"username": u})
        users = requests.get(B + "/list").json()["users"]
        if u not in users:
            misses += 1
    
    print("Consistency Test")
    print("misses:", misses, "out of", iters)

if __name__ == "__main__":
    latency_test(A, "A (us-central1)")
    latency_test(B, "B (europe-west1)")
    consistency_test(100)
