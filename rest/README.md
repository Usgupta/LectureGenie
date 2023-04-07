# Flask REST API documentation

## GET summaries/{id}

```
localhost:8000/summaries/{id}
```

## POST summaries

```
curl -X POST -H "Content-Type: application/json" -d '{"summary": "New summary"}' http://localhost:8000/summaries
```

## POST summaries/{id}/questions

```
curl -X POST -H "Content-Type: application/json" -d '{"questions": [{"question": "What is the summary about?", "answer": "The summary is about XYZ."}, {"question": "What are the main points?", "answer": "The main points are A, B, and C."}]}' http://localhost:8000/summaries/1/questions
```
