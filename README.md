# GourmetGirls

## Problem Statement
The advent of quick commerce has made ordering food easier than ever, leading to a decline in home cooking—especially of traditional, indigenous recipes that may disappear with our grandmothers’ generation. At the same time, people are becoming more health-conscious and budget-aware. What better way to address both than by suggesting recipes that make the most of what’s already in your fridge—while guiding you through your (or someone else’s) grandma’s special recipe?


## Solution
We aim to build a smart recipe assistant that can:
   * Suggest recipes using images of their fridge's contents.
   * Preserve indigenous recipes by recommending regional, lesser-known dishes within user groups with similar "tastes" (pun intended).
   * Guide users step-by-step through cooking via an interactive chatbot.

## Recommendation Engine
### Rule-based recommendation
1. User input
   1. Number of people you're cooking for
   2. Preferred cuisine/course
   3. Allergens if any
2. Image of (non)dairy ingredients available
3. Suggests recipes based on a formula, in which weightage given to different factors can be altered if need be.

### Collaborative-filtering based recommendation engine
1. Suggests recipes from users with similar interactions with recipes, ingredients and tags.
2. Current version has 42 synthesized recipes, and 20 users split into 5 groups of 4 each, with each group having roughly the same preferences.
3. Interactions of users with recipes have been simulated by calculating and selecting user-recipe pairs with high cosine-similarity (result of users liking/disliking a recipe)
4. Recommendation engine based on SVD has been trained on this dataset, which has RMSE of ~1.7


## Chatbot
### Corpus (Provided to the LLM for Context)
The corpus is a curated set of documents that provide essential cooking knowledge. It includes:

1. Mishap Handling Tips  
e.g., "Add a peeled raw potato to absorb excess salt"
2. General Cooking Tips  
e.g., "Fry onions till golden brown for richer gravies."
3. Common Food Swaps   
e.g., "No paneer? Use firm tofu"

### RAG 
RAG is an architecture that enhances LLMs by allowing them to retrieve relevant context from an **external corpus** before generating a response.
In our case, the chatbot:

1. Embeds the user query into a vector representation
2. Retrieves top-matching documents or text chunks from our recipe corpus using semantic similarity (e.g., via vector DB)
3. Feeds both the user query and the retrieved documents into the LLM
4. The LLM then generates a response that is grounded in the retrieved context
