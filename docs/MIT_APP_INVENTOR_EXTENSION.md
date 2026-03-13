# MIT App Inventor Chatbot Extension Guide

Complete walkthrough for creating a custom MIT App Inventor extension to import and use exported chatbot models.

## Overview

MIT App Inventor allows custom extensions (`.aix` files) to add new blocks and functionality. We'll create a ChatBot extension that:
- Loads exported JSON models
- Answers questions with keyword or semantic matching
- Updates dynamically as the model changes

## Architecture

```
MIT App Inventor App
    ↓
ChatBot Extension (.aix)
    ↓
Native Android/iOS Code
    ↓
Chatbot Model (JSON)
```

### Extension Components

1. **Blocks** - Designer UI elements
2. **Methods** - Java/Kotlin implementation
3. **Events** - Callbacks (e.g., `GotAnswer`)
4. **Properties** - Configuration (model path, threshold)

## Step 1: Extension Project Setup

### Requirements
- Java Development Kit (JDK 8+)
- App Inventor Extensions SDK
- Android SDK
- Your exported chatbot model JSON

### Directory Structure
```
ChatBotExtension/
├── src/
│   └── com/
│       └── chatbot/
│           └── ChatBot.java
├── build.xml
├── build.properties
└── lib/
    └── json.jar
```

## Step 2: Create the Extension Class

### Basic Extension Structure

```java
// ChatBot.java
package com.chatbot;

import android.content.Context;
import com.google.appinventor.components.annotations.*;
import com.google.appinventor.components.common.ComponentCategory;
import com.google.appinventor.components.runtime.AndroidNonvisibleComponent;
import com.google.appinventor.components.runtime.ComponentContainer;
import com.google.appinventor.components.runtime.EventDispatcher;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.*;
import java.util.*;

@DesignerComponent(
    version = 1,
    description = "Chatbot component for answering questions from JSON models",
    category = ComponentCategory.EXTENSION,
    nonVisible = true,
    iconName = "https://example.com/chatbot_icon.png"
)
@SimpleObject(external = true)
public class ChatBot extends AndroidNonvisibleComponent {
    
    private Context context;
    private JSONArray qaArray;
    private double similarityThreshold = 0.3;
    private String modelPath;
    private static final String TAG = "ChatBot";
    
    public ChatBot(ComponentContainer container) {
        super(container.$form());
        this.context = container.$context();
    }
    
    // PROPERTIES
    
    @DesignerProperty(editorType = PropertyEditorType.STRING,
                      defaultValue = "")
    @SimpleProperty(description = "Path to the chatbot model JSON file")
    public void ModelPath(String path) {
        modelPath = path;
    }
    
    @SimpleProperty(description = "Get the current model path")
    public String ModelPath() {
        return modelPath;
    }
    
    @DesignerProperty(editorType = PropertyEditorType.FLOAT,
                      defaultValue = "0.3")
    @SimpleProperty(description = "Minimum similarity threshold (0.0 to 1.0)")
    public void SimilarityThreshold(double threshold) {
        if (threshold >= 0 && threshold <= 1) {
            similarityThreshold = threshold;
        }
    }
    
    @SimpleProperty(description = "Get the similarity threshold")
    public double SimilarityThreshold() {
        return similarityThreshold;
    }
    
    // METHODS
    
    @SimpleFunction(description = "Load chatbot model from JSON file")
    public boolean LoadModel(String filePath) {
        try {
            String jsonContent = readFile(filePath);
            JSONObject model = new JSONObject(jsonContent);
            qaArray = model.getJSONArray("qa_pairs");
            modelPath = filePath;
            ModelLoaded(true);
            return true;
        } catch (Exception e) {
            ModelError("Failed to load model: " + e.getMessage());
            return false;
        }
    }
    
    @SimpleFunction(description = "Get answer to a question")
    public String GetAnswer(String question) {
        if (qaArray == null) {
            ModelError("Model not loaded");
            return "";
        }
        
        try {
            Map<String, Object> result = findBestMatch(question);
            String answer = (String) result.get("answer");
            double confidence = (double) result.get("confidence");
            String originalQuestion = (String) result.get("question");
            
            // Trigger event with details
            GotAnswer(answer, confidence, originalQuestion);
            return answer;
        } catch (Exception e) {
            ModelError("Error getting answer: " + e.getMessage());
            return "";
        }
    }
    
    @SimpleFunction(description = "Get similar questions from knowledge base")
    public String GetSimilarQuestions(String question, int topK) {
        if (qaArray == null) {
            ModelError("Model not loaded");
            return "[]";
        }
        
        try {
            List<Map<String, Object>> similar = findSimilarQuestions(question, topK);
            JSONArray result = new JSONArray();
            
            for (Map<String, Object> item : similar) {
                JSONObject obj = new JSONObject();
                obj.put("question", item.get("question"));
                obj.put("score", item.get("score"));
                result.put(obj);
            }
            
            return result.toString();
        } catch (Exception e) {
            ModelError("Error getting similar questions: " + e.getMessage());
            return "[]";
        }
    }
    
    @SimpleFunction(description = "Search for Q&A by keyword")
    public String SearchByKeyword(String keyword) {
        if (qaArray == null) {
            ModelError("Model not loaded");
            return "[]";
        }
        
        try {
            JSONArray results = new JSONArray();
            String keywordLower = keyword.toLowerCase();
            
            for (int i = 0; i < qaArray.length(); i++) {
                JSONObject qa = qaArray.getJSONObject(i);
                String question = qa.getString("question").toLowerCase();
                String answer = qa.getString("answer").toLowerCase();
                
                if (question.contains(keywordLower) || answer.contains(keywordLower)) {
                    results.put(qa);
                }
            }
            
            return results.toString();
        } catch (Exception e) {
            ModelError("Error searching: " + e.getMessage());
            return "[]";
        }
    }
    
    @SimpleFunction(description = "Get total number of Q&A pairs")
    public int GetQAPairCount() {
        return qaArray != null ? qaArray.length() : 0;
    }
    
    @SimpleFunction(description = "Get all Q&A pairs as JSON")
    public String GetAllQAPairs() {
        if (qaArray == null) {
            return "[]";
        }
        return qaArray.toString();
    }
    
    // EVENTS
    
    @SimpleEvent(description = "Triggered when model is loaded successfully")
    public void ModelLoaded(boolean success) {
        EventDispatcher.dispatchEvent(this, "ModelLoaded", success);
    }
    
    @SimpleEvent(description = "Triggered when answer is retrieved")
    public void GotAnswer(String answer, double confidence, String originalQuestion) {
        EventDispatcher.dispatchEvent(this, "GotAnswer", answer, confidence, originalQuestion);
    }
    
    @SimpleEvent(description = "Triggered when error occurs")
    public void ModelError(String errorMessage) {
        EventDispatcher.dispatchEvent(this, "ModelError", errorMessage);
    }
    
    // HELPER METHODS
    
    private String readFile(String filePath) throws IOException {
        StringBuilder content = new StringBuilder();
        BufferedReader reader = new BufferedReader(new FileReader(filePath));
        String line;
        while ((line = reader.readLine()) != null) {
            content.append(line);
        }
        reader.close();
        return content.toString();
    }
    
    private Map<String, Object> findBestMatch(String question) throws Exception {
        String questionLower = question.toLowerCase();
        String[] questionWords = questionLower.split("\\s+");
        Set<String> questionSet = new HashSet<>(Arrays.asList(questionWords));
        
        double bestScore = 0;
        String bestAnswer = "";
        String bestQuestion = "";
        
        for (int i = 0; i < qaArray.length(); i++) {
            JSONObject qa = qaArray.getJSONObject(i);
            String qaQuestion = qa.getString("question").toLowerCase();
            String[] qaWords = qaQuestion.split("\\s+");
            Set<String> qaSet = new HashSet<>(Arrays.asList(qaWords));
            
            // Calculate Jaccard similarity
            Set<String> intersection = new HashSet<>(questionSet);
            intersection.retainAll(qaSet);
            
            Set<String> union = new HashSet<>(questionSet);
            union.addAll(qaSet);
            
            double similarity = (double) intersection.size() / union.size();
            
            if (similarity > bestScore) {
                bestScore = similarity;
                bestAnswer = qa.getString("answer");
                bestQuestion = qa.getString("question");
            }
        }
        
        Map<String, Object> result = new HashMap<>();
        result.put("answer", bestAnswer);
        result.put("confidence", bestScore);
        result.put("question", bestQuestion);
        return result;
    }
    
    private List<Map<String, Object>> findSimilarQuestions(String question, int topK) throws Exception {
        List<Map<String, Object>> results = new ArrayList<>();
        String questionLower = question.toLowerCase();
        String[] questionWords = questionLower.split("\\s+");
        Set<String> questionSet = new HashSet<>(Arrays.asList(questionWords));
        
        for (int i = 0; i < qaArray.length(); i++) {
            JSONObject qa = qaArray.getJSONObject(i);
            String qaQuestion = qa.getString("question").toLowerCase();
            String[] qaWords = qaQuestion.split("\\s+");
            Set<String> qaSet = new HashSet<>(Arrays.asList(qaWords));
            
            Set<String> intersection = new HashSet<>(questionSet);
            intersection.retainAll(qaSet);
            Set<String> union = new HashSet<>(questionSet);
            union.addAll(qaSet);
            
            double similarity = (double) intersection.size() / union.size();
            
            if (similarity >= similarityThreshold) {
                Map<String, Object> item = new HashMap<>();
                item.put("question", qa.getString("question"));
                item.put("answer", qa.getString("answer"));
                item.put("score", similarity);
                results.add(item);
            }
        }
        
        // Sort by score descending
        results.sort((a, b) -> Double.compare((double)b.get("score"), (double)a.get("score")));
        
        // Return top K
        return results.subList(0, Math.min(topK, results.size()));
    }
}
```

## Step 3: Extension Blocks Available in MIT App Inventor

Once the extension is built and installed, designers see these blocks:

### Properties Blocks
- **set ChatBot.ModelPath to** → Configure model file location
- **set ChatBot.SimilarityThreshold to** → Adjust matching strictness (0-1)

### Method Blocks
- **call ChatBot.LoadModel** → Load JSON model from file
- **call ChatBot.GetAnswer** → Get answer to question
- **call ChatBot.GetSimilarQuestions** → Find similar questions
- **call ChatBot.SearchByKeyword** → Search Q&A pairs
- **call ChatBot.GetQAPairCount** → Count Q&A pairs
- **call ChatBot.GetAllQAPairs** → Get all Q&A as JSON

### Event Blocks
- **when ChatBot.ModelLoaded** → Detects model loaded
- **when ChatBot.GotAnswer** → Receives answer with confidence
- **when ChatBot.ModelError** → Handles errors

## Step 4: Building the Extension

### Using MIT App Inventor Build System

```bash
# Clone App Inventor extensions templates
git clone https://github.com/mit-cml/app-inventor-extensions.git

# Copy your ChatBot.java to templates/extensions/
cp ChatBot.java templates/extensions/com/chatbot/

# Build
cd templates/extensions/
ant extensions

# Output: ChatBot.aix
```

### Alternative: Using App Inventor Online Editor

1. Upload `.java` file directly to MIT App Inventor
2. System automatically compiles to `.aix`
3. Ready to import into projects

## Step 5: Using in MIT App Inventor Designer

### Step 1: Import Extension
1. Open MIT App Inventor project
2. Click "Extension" in Components panel
3. Select "Import extension (.aix file)"
4. Choose your `ChatBot.aix`
5. ChatBot component appears in Designer

### Step 2: Add to Screen
1. Drag ChatBot component to Screen
2. Appears as non-visible component
3. Now blocks are available in Blocks editor

### Step 3: Configure in Blocks

```blocks
// Initialize
when Screen.Initialize
  set ChatBot.ModelPath to "/storage/emulated/0/Download/chatbot_model.json"
  set ChatBot.SimilarityThreshold to 0.4
  call ChatBot.LoadModel ChatBot.ModelPath

// Handle loaded event
when ChatBot.ModelLoaded success
  set global qaCount to call ChatBot.GetQAPairCount
  call Label.setText join "Loaded " qaCount " Q&A pairs"

// Get answer on button click
when AskButton.Click
  set userQuestion to call TextBox.Text
  call ChatBot.GetAnswer userQuestion

// Handle answer event
when ChatBot.GotAnswer answer confidence originalQuestion
  set Label_Answer.Text to answer
  set Label_Confidence.Text to join "Confidence: " confidence
  set Label_Question.Text to join "Matched: " originalQuestion

// Handle errors
when ChatBot.ModelError errorMessage
  call Notifier.ShowMessageDialog errorMessage "Error"
```

## Step 6: Complete App Example

### UI Layout (Designer View)
```
Screen
├── VerticalArrangement
│   ├── Label "Chat Bot Assistant"
│   ├── TextBox (user_question)
│   ├── Button "Ask"
│   ├── Label "Answer:"
│   ├── Label (answer_display)
│   ├── Label "Confidence: "
│   ├── Label (confidence_display)
│   └── Button "Search"
├── ChatBot (component)
└── ListPicker (for similar questions)
```

### Blocks Logic

```
[Initialize]
  → Load model
  → Display status

[AskButton.Click]
  → Get question from TextBox
  → Call GetAnswer
  → Display result

[GotAnswer event]
  → Update UI with answer
  → Show confidence
  → Log interaction

[SearchButton.Click]
  → Get keyword
  → Call SearchByKeyword
  → Display results in list
```

## Step 7: Managing Model Files

### File Storage Options

1. **App Assets** (Best for static models)
   ```
   Assets folder in MIT App Inventor
   → model.json
   ```
   
2. **Device Storage** (Best for updates)
   ```
   /storage/emulated/0/Download/model.json
   /storage/emulated/0/Documents/chatbot/model.json
   ```

3. **Cloud Storage** (Best for sync)
   ```
   Download from API:
   → /api/export/lightweight/<id>
   → /api/export/embedding/<id>
   ```

### Implementation: Downloading Model

```blocks
when UpdateModelButton.Click
  set global url to "https://api.example.com/api/export/lightweight/chatbot_1"
  call Web1.Get url

when Web1.GotText response
  // Write to file
  set global modelPath to "/storage/emulated/0/Download/chatbot_model.json"
  // Use Device storage methods or File component
  call ChatBot.LoadModel modelPath
```

## Step 8: Advanced Features

### Real-time Model Updates

```java
// In extension
@SimpleFunction(description = "Update Q&A pair")
public void UpdateQAPair(int index, String question, String answer) {
    try {
        if (index >= 0 && index < qaArray.length()) {
            JSONObject qa = qaArray.getJSONObject(index);
            qa.put("question", question);
            qa.put("answer", answer);
            QAPairUpdated(index);
        }
    } catch (Exception e) {
        ModelError("Error updating Q&A: " + e.getMessage());
    }
}

@SimpleEvent(description = "Q&A pair was updated")
public void QAPairUpdated(int index) {
    EventDispatcher.dispatchEvent(this, "QAPairUpdated", index);
}
```

### Batch Processing

```java
@SimpleFunction(description = "Get answers to multiple questions")
public String GetAnswersForBatch(String questionsJson) {
    try {
        JSONArray questions = new JSONArray(questionsJson);
        JSONArray results = new JSONArray();
        
        for (int i = 0; i < questions.length(); i++) {
            String question = questions.getString(i);
            Map<String, Object> result = findBestMatch(question);
            
            JSONObject answerObj = new JSONObject();
            answerObj.put("question", question);
            answerObj.put("answer", result.get("answer"));
            answerObj.put("confidence", result.get("confidence"));
            results.put(answerObj);
        }
        
        return results.toString();
    } catch (Exception e) {
        ModelError("Batch processing error: " + e.getMessage());
        return "[]";
    }
}
```

### Semantic Similarity (with Libraries)

```java
// Add sentiment analysis library
import edu.stanford.nlp.pipeline.*;

@SimpleFunction(description = "Get semantic similarity score")
public double GetSemanticSimilarity(String text1, String text2) {
    // Requires Stanford NLP or similar library
    // Would use embeddings for real implementation
    return calculateSimilarity(text1, text2);
}
```

## Step 9: Performance Optimization

### Caching

```java
private Map<String, List<String>> searchCache = new HashMap<>();

@SimpleFunction(description = "Search with caching")
public String SearchByKeywordCached(String keyword) {
    if (searchCache.containsKey(keyword)) {
        return searchCache.get(keyword).toString();
    }
    
    String results = SearchByKeyword(keyword);
    // Store in cache
    return results;
}

@SimpleFunction(description = "Clear cache")
public void ClearCache() {
    searchCache.clear();
}
```

### Lazy Loading

```java
private boolean modelLoaded = false;

@SimpleFunction(description = "Lazy load model on first use")
public String GetAnswerLazy(String question) {
    if (!modelLoaded) {
        LoadModel(modelPath);
        modelLoaded = true;
    }
    return GetAnswer(question);
}
```

## Step 10: Testing the Extension

### Unit Tests

```java
@Test
public void testLoadModel() {
    ChatBot chatbot = new ChatBot(container);
    boolean loaded = chatbot.LoadModel("test_model.json");
    assertTrue(loaded);
}

@Test
public void testGetAnswer() {
    chatbot.LoadModel("test_model.json");
    String answer = chatbot.GetAnswer("What is Python?");
    assertNotNull(answer);
    assertFalse(answer.isEmpty());
}

@Test
public void testSimilarityThreshold() {
    chatbot.SimilarityThreshold(0.5);
    assertEquals(0.5, chatbot.SimilarityThreshold());
}
```

## Complete Workflow

### 1. Export Chatbot Model
```bash
python export_chatbot_model.py
# Creates: chatbot_lightweight.json (3.6 KB)
```

### 2. Build Extension
```bash
ant extensions
# Creates: ChatBot.aix
```

### 3. Create MIT App Inventor App
- Import ChatBot.aix
- Add ChatBot component
- Design UI
- Write blocks

### 4. Deploy to Mobile
- Build APK in MIT App Inventor
- Install on Android device
- App loads chatbot_model.json
- Chat works offline!

## Architecture Diagram

```
┌─────────────────────────────────────┐
│   MIT App Inventor Designer         │
│  (Visual block programming)         │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   ChatBot Extension (ChatBot.aix)   │
│  - LoadModel()                      │
│  - GetAnswer()                      │
│  - GetSimilarQuestions()            │
│  - SearchByKeyword()                │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   Android Runtime                   │
│  - File I/O                         │
│  - JSON parsing                     │
│  - Event handling                   │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│   Chatbot Model (JSON)              │
│  {                                  │
│    "qa_pairs": [...]                │
│  }                                  │
└─────────────────────────────────────┘
```

## Troubleshooting

### Model Not Loading
```
Problem: LoadModel returns false
Solution: 
  1. Check file path is correct
  2. Verify JSON is valid (python -m json.tool model.json)
  3. Check file permissions
  4. Use error event to get detailed message
```

### Low Accuracy
```
Problem: GetAnswer returns no match
Solution:
  1. Lower SimilarityThreshold
  2. Use GetSimilarQuestions instead
  3. Check Q&A pairs loaded with GetQAPairCount
  4. Consider using embedding model
```

### Extension Not Appearing
```
Problem: ChatBot component not in Designer
Solution:
  1. Ensure .aix file is valid
  2. Reimport extension
  3. Restart MIT App Inventor
  4. Check for compilation errors
```

## Resources

- [MIT App Inventor Extension Development](http://appinventor.mit.edu/explore/extension-documentation)
- [App Inventor Extension Template](https://github.com/mit-cml/app-inventor-extensions)
- [Android File I/O Documentation](https://developer.android.com/guide/topics/data/data-storage)
- [JSON Parsing in Android](https://developer.android.com/reference/org/json/JSONObject)

## Next Steps

1. Build the extension: `ant extensions`
2. Test with sample model
3. Deploy to MIT App Inventor
4. Create chatbot app
5. Export as APK
6. Test on mobile device

This creates a complete integration between exported chatbot models and MIT App Inventor, enabling offline chatbot apps for Android!
