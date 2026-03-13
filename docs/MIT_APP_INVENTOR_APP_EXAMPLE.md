# MIT App Inventor Chatbot App - Complete Example

Step-by-step tutorial for building a complete chatbot app in MIT App Inventor using the ChatBot extension.

## Project Overview

**App Name:** ChatBot Assistant  
**Target:** Android devices  
**Features:**
- Load chatbot model from JSON
- Ask questions and get answers
- Search knowledge base
- View similar questions
- Offline capability

## Step 1: App Structure

```
ChatBotAssistant/
├── Screens
│   ├── MainScreen (home, chat interface)
│   ├── SearchScreen (knowledge base search)
│   └── SettingsScreen (model management)
├── Components
│   └── ChatBot extension
├── Assets
│   └── chatbot_lightweight.json
└── Blocks
    ├── Screen initialization
    ├── Button click handlers
    └── Event handlers
```

## Step 2: Designer Layout (MainScreen)

### Component Hierarchy

```
Screen1 (MainScreen)
│
├── VerticalArrangement (mainLayout)
│   │
│   ├── HorizontalArrangement (headerLayout)
│   │   └── Label "🤖 ChatBot Assistant"
│   │
│   ├── HorizontalArrangement (statusLayout)
│   │   ├── Label "Status: "
│   │   └── Label "Initializing..." (statusLabel)
│   │
│   ├── VerticalArrangement (chatLayout)
│   │   ├── Label "Question:"
│   │   ├── TextBox (questionInput)
│   │   │   └── Hint: "Ask me anything..."
│   │   │
│   │   ├── Button "Ask" (askButton)
│   │   │
│   │   ├── Label "Answer:"
│   │   ├── Label "" (answerDisplay)
│   │   │   └── FontSize: 16
│   │   │   └── TextColor: Green
│   │   │
│   │   ├── HorizontalArrangement
│   │   │   ├── Label "Confidence: "
│   │   │   └── Label "0%" (confidenceDisplay)
│   │   │
│   │   ├── HorizontalArrangement
│   │   │   ├── Label "Matched: "
│   │   │   └── Label "" (matchedDisplay)
│   │
│   ├── ListView (chatHistory)
│   │   └── Shows Q&A history
│   │
│   └── HorizontalArrangement (buttonLayout)
│       ├── Button "Search" (searchButton)
│       ├── Button "Settings" (settingsButton)
│       └── Button "Clear" (clearButton)
│
├── ChatBot (component, non-visible)
│
├── Notifier (for alerts)
│
└── File (for model management)
```

### Component Properties

| Component | Property | Value |
|-----------|----------|-------|
| MainLayout | Orientation | Vertical |
| | Width | Fill parent |
| | Height | Fill parent |
| StatusLabel | Text | "Ready" |
| | TextSize | 14 |
| QuestionInput | Hint | "Ask a question..." |
| | MultiLine | false |
| AnswerDisplay | FontSize | 16 |
| | TextColor | #006633 (green) |
| ConfidenceDisplay | TextSize | 12 |
| ChatHistory | Height | 200 pixels |
| | Width | Fill parent |

## Step 3: Blocks - Initialization

```blocks
// Initialize
when Screen1.Initialize
  
  // Show loading
  set statusLabel.Text to "⏳ Loading model..."
  
  // Set model path
  // For assets: file:///android_asset/chatbot_lightweight.json
  // For device: /storage/emulated/0/Download/chatbot_model.json
  set global MODEL_PATH to "/storage/emulated/0/Download/chatbot_lightweight.json"
  
  // Configure ChatBot
  set ChatBot.SimilarityThreshold to 0.3
  
  // Load model (on separate thread)
  call ChatBot.LoadModel (global MODEL_PATH)

when ChatBot.ModelLoaded success
  
  if success then
    set statusLabel.Text to join "✓ Ready (" (call ChatBot.GetQAPairCount) " Q&A)"
    set answerDisplay.Text to "Ready to answer questions"
  else
    set statusLabel.Text to "✗ Model failed to load"

when ChatBot.ModelError errorMessage
  call Notifier.ShowMessageDialog errorMessage "Error Loading Model"
```

## Step 4: Blocks - Ask Question Handler

```blocks
when askButton.Click
  
  // Get user input
  set global userQuestion to questionInput.Text
  
  // Validate
  if (is userQuestion empty?) then
    call Notifier.ShowAlert "Please enter a question"
    exit function
  
  // Show loading
  set answerDisplay.Text to "⏳ Finding answer..."
  
  // Request answer
  call ChatBot.GetAnswer (global userQuestion)

when ChatBot.GotAnswer answer confidence originalQuestion
  
  // Update UI
  set answerDisplay.Text to answer
  set confidenceDisplay.Text to join (round (* confidence 100)) "%"
  set matchedDisplay.Text to originalQuestion
  
  // Add to history
  call addChatToHistory (global userQuestion) (answer) (confidence)
  
  // Clear input
  set questionInput.Text to ""
  
  // Show notification if confidence is low
  if (< confidence 0.5) then
    call Notifier.ShowMessageDialog 
      "Low confidence match. Try searching similar questions." 
      "Tip"
```

## Step 5: Blocks - Add Chat to History

```blocks
procedure addChatToHistory question answer confidence
  
  // Format entry
  set global entry to call join 
    "Q: " question newline
    "A: " answer newline
    "Score: " (round (* confidence 100)) "%" newline
    "---" newline
  
  // Get current history
  set global currentHistory to chatHistory.Text
  
  // Add new entry
  set chatHistory.Text to call join currentHistory entry
  
  // Optional: Save to persistent storage
  call File.SaveText (join "/storage/emulated/0/chatbot_history_" (current-time) ".txt") 
    (call join currentHistory entry)
```

## Step 6: Blocks - Search Knowledge Base

```blocks
when searchButton.Click
  
  // Get search term
  set global searchKeyword to call Notifier.ShowTextDialog 
    "Search for:" 
    ""
  
  if (is searchKeyword empty?) then
    exit function
  
  set answerDisplay.Text to "🔍 Searching..."
  
  // Perform search
  set global searchResults to call ChatBot.SearchByKeyword (global searchKeyword)
  
  // Parse and display results
  call displaySearchResults (global searchResults)

procedure displaySearchResults resultsJson
  
  set answerDisplay.Text to call join 
    "Found " (count-items resultsJson) " results for '" (global searchKeyword) "'"
  
  // Create formatted list
  set global resultsList to ""
  
  for each item in resultsJson
    set global resultsList to call join 
      (global resultsList)
      "Q: " (item "question") newline
      "A: " (item "answer") newline
      "---" newline
  
  set chatHistory.Text to (global resultsList)
```

## Step 7: Blocks - Similar Questions

```blocks
when chatHistory.Selection changed
  
  // Get selected item
  set global selectedIndex to chatHistory.SelectionIndex
  
  if (> (global selectedIndex) 0) then
    
    // Extract question from selected item
    set global selectedQuestion to call parseQuestionFromItem (chatHistory.Selection)
    
    // Get similar
    set global similarJSON to call ChatBot.GetSimilarQuestions 
      (global selectedQuestion) 
      3
    
    // Display similar
    call displaySimilarQuestions (global similarJSON) (global selectedQuestion)

procedure displaySimilarQuestions similarJson originalQuestion
  
  set answerDisplay.Text to call join 
    "Questions similar to: " newline
    "'" originalQuestion "'" newline newline
  
  set global similarText to ""
  
  for each item in similarJson
    set global similarText to call join
      (global similarText)
      "• " (item "question") newline
      "  Similarity: " (round (* (item "score") 100)) "%" newline
  
  set chatHistory.Text to (global similarText)
```

## Step 8: Blocks - Settings Screen

```blocks
// Settings Button Handler
when settingsButton.Click
  open another screen SettingsScreen

// Settings Screen - Component Selection
when SettingsScreen.Initialize
  
  set global thresholdSlider.ThumbPosition to 30 // 0-100 scale
  set global thresholdLabel.Text to "Threshold: 0.3"
  
  set global modelPathLabel.Text to (global MODEL_PATH)
  
  set global qaPairCountLabel.Text to join 
    "Q&A Pairs: " (call ChatBot.GetQAPairCount)

// Threshold Changed
when thresholdSlider.ThumbPosition changed
  
  set global newThreshold to (/ (global thresholdSlider.ThumbPosition) 100)
  set ChatBot.SimilarityThreshold to (global newThreshold)
  set thresholdLabel.Text to join "Threshold: " (global newThreshold)
  call Notifier.ShowAlert "Threshold updated"

// Update Model Button
when updateModelButton.Click
  
  set statusLabel.Text to "Downloading model..."
  
  // Download from API
  set global apiUrl to "https://api.example.com/api/export/lightweight/chatbot_1"
  
  call Web1.Get (global apiUrl)

when Web1.GotText responseContent
  
  // Save to device
  set global newModelPath to "/storage/emulated/0/Download/chatbot_model.json"
  
  // Use file component (requires special handling for JSON)
  call File.SaveText (global newModelPath) (responseContent)
  
  // Reload model
  call ChatBot.LoadModel (global newModelPath)
  set global MODEL_PATH to (global newModelPath)
```

## Step 9: Blocks - Clear History

```blocks
when clearButton.Click
  
  // Confirm
  call Notifier.ShowChooseDialog 
    "Clear chat history?" 
    "Clear" 
    "Cancel" 
    "Confirm"

when Notifier.AfterChoosing response
  if (= response "Clear") then
    set chatHistory.Text to ""
    set answerDisplay.Text to ""
    set confidenceDisplay.Text to ""
    set matchedDisplay.Text to ""
    call Notifier.ShowAlert "History cleared"
```

## Step 10: Helper Procedures

```blocks
// Parse question from chat entry
procedure parseQuestionFromItem chatItem
  set global lines to call split-text chatItem "Q: "
  set global afterQ to select-list-item (global lines) 2
  set global lines2 to call split-text (global afterQ) "newline"
  return select-list-item (global lines2) 1

// Format confidence as percentage
procedure formatConfidence confidence
  return call join (round (* confidence 100)) "%"

// Get timestamp for logging
procedure getTimestamp
  return call join 
    (current-date-time) 
    " - "

// Save chat session
procedure saveChatSession
  set global sessionFile to join 
    "/storage/emulated/0/chatbot_session_"
    (replace-all (call clock1.FormatTime (call clock1.Now)) ":" "-")
    ".txt"
  
  call File.SaveText (global sessionFile) (chatHistory.Text)
```

## Step 11: Advanced Features

### Real-time Search as User Types

```blocks
when questionInput.TextChanged newText
  
  // Only search if text length > 3
  if (>= (length newText) 3) then
    
    // Debounce (wait for user to stop typing)
    if (< (- (call clock1.Now) (global lastSearchTime)) 500) then
      exit function
    
    set global lastSearchTime to (call clock1.Now)
    
    // Show suggestions
    set global suggestions to call ChatBot.SearchByKeyword (newText)
    
    call displaySuggestions (global suggestions)
```

### Rating System

```blocks
when ratingBar.RatingChanged rating
  
  // Save rating
  set global lastRating to rating
  
  if (>= rating 4) then
    call Notifier.ShowAlert "Thanks for the positive feedback!"
  else
    call Notifier.ShowChooseDialog
      "We're sorry. How can we improve?"
      "Report Issue"
      "Cancel"
      "Report"
```

### Export Chat Session

```blocks
when exportButton.Click
  
  set global timestamp to (call clock1.FormatTime (call clock1.Now))
  set global filename to join 
    "/storage/emulated/0/chatbot_session_"
    (replace-all timestamp ":" "-")
    ".txt"
  
  call File.SaveText (global filename) (chatHistory.Text)
  call Notifier.ShowAlert (join "Saved to " (global filename))
```

## Complete Block Diagram

```
Startup
  ↓
[Initialize]
  ├→ Set MODEL_PATH
  ├→ Create ChatBot
  └→ Load Model
     ↓
  [ModelLoaded]
     └→ Set Status "Ready"

User Input (Ask Button)
  ↓
[Check Input]
  ├→ Validate not empty
  ├→ Call GetAnswer
  └→ Show "Loading..."
     ↓
  [GotAnswer Event]
     ├→ Display answer
     ├→ Show confidence
     ├→ Add to history
     └→ Update matched Q

User Input (Search Button)
  ↓
[Get Search Term]
  ├→ Call SearchByKeyword
  └→ Display results

User Input (Settings Button)
  ↓
[Open Settings Screen]
  ├→ Adjust threshold
  ├→ Update model
  └→ View stats
```

## File Structure

```
Assets/
├── chatbot_lightweight.json
├── chatbot_icon.png
└── README.txt

Device Storage/
├── /storage/emulated/0/Download/
│   └── chatbot_lightweight.json
├── /storage/emulated/0/chatbot_sessions/
│   └── chatbot_session_*.txt
└── /storage/emulated/0/chatbot_logs/
    └── chatbot_*.log
```

## Permissions Required

Add to AndroidManifest.xml:

```xml
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.INTERNET" />
```

## Testing Checklist

- [ ] App starts without errors
- [ ] Model loads successfully
- [ ] Can ask questions and get answers
- [ ] Confidence scores display correctly
- [ ] Search functionality works
- [ ] Similar questions found
- [ ] Threshold adjustment works
- [ ] Chat history saves
- [ ] Settings persist
- [ ] Model updates work
- [ ] App works offline (after model loads)
- [ ] Performance acceptable on low-end device

## Deployment

### Build APK
1. In MIT App Inventor: **Package** → **APK**
2. Wait for build to complete
3. Download .apk file

### Install on Device
```bash
adb install ChatBotAssistant.apk
```

Or:
1. Copy .apk to device
2. Open file manager
3. Tap to install
4. Grant permissions

### Google Play Deployment
1. Create Google Play Developer account
2. Upload APK
3. Submit for review
4. Publish

## Troubleshooting

### App Crashes on Start
- Check ChatBot.aix is properly imported
- Verify assets are included
- Check permissions in manifest

### Model Not Loading
- Verify file path is correct
- Check JSON validity
- Ensure file permissions set to readable

### No Answers Found
- Lower similarity threshold
- Verify Q&A pairs loaded (check count)
- Check question format matches training data

## Performance Tips

1. **Cache results** for repeated questions
2. **Lazy load** model on first use
3. **Limit history** to prevent memory issues
4. **Use lightweight** model for mobile
5. **Background threads** for file operations

## Next Steps

1. Export your chatbot model
2. Import ChatBot.aix extension
3. Build this app in MIT App Inventor
4. Test on Android device
5. Customize design and features
6. Deploy to Google Play

This creates a complete, production-ready chatbot application for Android!
