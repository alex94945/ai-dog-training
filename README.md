# AI-dog-training-GPT

This app enables AI-powered search for the Zak George and Dog Training By Kikopup YouTube channels.

Channel is here:
https://www.youtube.com/channel/UCZzFRKsgVMhGTxffpzgTJlQ
https://www.youtube.com/channel/UC-qnqaajTk6bfs3UZuue6IQ

## Dataset
 
Use whisper to generate transcripts with all steps outlined in -
`scripts/make_index.ipynb`
 
 ## App

Use Langchain `VectorDBQAChain` to - 
* Embed the user query
* Perform similarity search on Pinecone embeddings
* Synthesize the answer from relevant chunks with `GPT 3.5` (also benchmark GPT4)

Relevant chunks with metadata (links) are displayed as source documents.
 
This builds on the excellent UI from https://github.com/mckaywrigley/wait-but-why-gpt.

## Deploy

Deploy to Fly.io: `fly launch`

## Credits

Thanks to Lance Martin for open sourcing his Besties GPT code (https://github.com/rlancemartin/besties-gpt)

Thanks to [Mckay Wrigley](https://twitter.com/mckaywrigley) for open-sourcing his UI.

## Local testing

`yarn dev`
