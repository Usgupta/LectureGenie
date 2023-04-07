import http.client
import json

conn = http.client.HTTPSConnection("api.pawan.krd")

    # "prompt": "Convert the following lecture transcript into question and answers: Testosterone is a chemical substance known as a hormone and it can have quite wide-ranging effects through the body and that’s because it’s released into the bloodstream and therefore it can go around the body in the blood circulation and affect a wide range of organs.Testosterone is made in males in Leydig cells in the testes.There’s also a small amount made in the ovaries in females,and in both sexes is made in the adrenal glands which sits on top of the kidneys.Now, the release of testosterone is controlled by a group of structures called the hypothalamic-pituitary-adrenal axis, and these include the hypothalamus in the brain, the pituitary gland at the base of the brain, and the adrenal glands on top of the kidneys.The release of testosterone generally occurs in two quite big surges in the body and these happen at around seven weeks of fetal development,and that’s associated with the development of the male genitalia,and it happens again at around age twelve and that’s associated with puberty.So as well as those physical characteristics, the release of testosterone is also associated with larger body bills,increased muscle mass and more and more bodily hair.But it’s also associated with some interesting psychological characteristics as well,and these include, greater aggression, more dominant behaviour, but also really interesting behaviour known as risk-taking.",

payload = json.dumps({
    "model": "text-davinci-003",
    "prompt": "Convert the following lecture transcript into question and answers: https://www.youtube.com/watch?v=dQw4w9WgXcQ.",
    "temperature": 0.2,
    "max_tokens": 256,
    "stop": [
        "Human:",
        "AI:"
    ]
})

headers = {
    'Authorization': 'Bearer pk-KRnpVmvJKalEqmFseSighmlOoMyIohZiIHwFRqjNIXeylZXR',
    'Content-Type': 'application/json'
}

conn.request("POST", "/v1/completions", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
