from encrypt_decrypt import encode, decode
from freq_attack import Attack

plaintext = "If you're looking for random paragraphs, you've come to the right place. When a random word or a random sentence isn't quite enough, the next logical step is to find a random paragraph. We created the Random Paragraph Generator with you in mind. The process is quite simple. Choose the number of random paragraphs you'd like to see and click the button. Your chosen number of paragraphs will instantly appear.While it may not be obvious to everyone, there are a number of reasons creating random paragraphs can be useful. A few examples of how some people use this generator are listed in the following paragraphs."
key = "keyword"

encoded = encode(plaintext, key)
decoded = decode(encoded, key)

print(encoded)
print(decoded)

with open("data/encrypted_text/newly_encoded.txt", "w") as f:
    f.write(encoded)

attack = Attack("newly_encoded.txt")
attack.brute_force(20)
