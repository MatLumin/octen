import hashlib;

data = "uwu";
nonce = 0;
h = hashlib.new("sha256")

while True:
    h.update((data+str(nonce)).encode("utf-8"));
    d = h.hexdigest()
    d2 = list(d);
    count = d2.count("0");
    if count > 13:
        print("owo");
    nonce += 1;