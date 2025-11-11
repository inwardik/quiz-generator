# Quiz Generator

Interactive HTML quiz generator from Markdown files.

## Features

### Core Features

- **Standalone HTML** - all styles and scripts embedded in one file
- **Modern Design** - beautiful responsive interface with gradient accents
- **Dark Theme** - toggle between light and dark themes
- **Progress Bar** - visual progress tracking
- **Score Tracking** - real-time score updates
- **Final Results** - detailed statistics on completion
- **Mobile Responsive** - works perfectly on all devices
- **No Dependencies** - no Bootstrap or other libraries needed
- **Privacy First** - no data sent to servers
- **Random Order** - questions and answers randomized on each page load

### Quiz Functions

- Shuffle questions (optional during generation)
- Shuffle answers (optional during generation)
- Dynamic randomization on page load
- Instant feedback on answers
- Show correct answers on errors
- Restart quiz option
- Theme preference saved in localStorage

## Requirements

Python 3.6 or higher. No external dependencies!

## Installation

Simply copy the `to_html.py` file to your directory.

## Usage

### Basic Usage

```bash
python to_html.py quiz.md
```

This will create a `quiz.html` file in the same directory.

### Command Line Options

```bash
# Specify output file name
python to_html.py quiz.md -o my-quiz.html

# Disable question shuffling during generation
python to_html.py quiz.md --no-shuffle-questions

# Disable answer shuffling during generation
python to_html.py quiz.md --no-shuffle-answers

# Enable dark mode by default
python to_html.py quiz.md --dark-mode

# Combine options
python to_html.py quiz.md -o output.html --no-shuffle-questions --dark-mode
```

### Help

```bash
python to_html.py --help
```

## Quiz Markdown Format

### File Structure

```markdown
## Quiz Title

#### Question 1 text

- [ ] Wrong answer 1
- [x] Correct answer
- [ ] Wrong answer 2
- [ ] Wrong answer 3

#### Question 2 text

- [ ] Wrong answer
- [x] Correct answer 1
- [x] Correct answer 2
- [ ] Wrong answer
```

### Formatting Rules

1. **Quiz Title** - use `## Title` (h2) at the beginning
2. **Questions** - start with `####` (h4) or `###` (h3)
3. **Answers** - checkbox list:
   - `- [ ]` - wrong answer
   - `- [x]` or `- [X]` - correct answer
4. **Multiple Correct Answers** - supported, use multiple `[x]`

### Example

See `quiz.md` file in this directory for a complete example with 15 Python questions.

## Implementation Details

### Technical Details

- **Parsing** - regular expressions for reliable Markdown parsing
- **HTML/CSS/JS** - all embedded in one file for portability
- **Responsive Design** - CSS Grid and Flexbox
- **Dark Theme** - CSS variables for easy switching
- **LocalStorage** - saves theme preferences and handles mobile state
- **Validation** - structure checking before generation

### Code Architecture

- `QuizParser` - class for Markdown parsing
- `HTMLGenerator` - class for HTML generation
- `main()` - command line argument handling

## Usage Examples

### Create Quiz for Educational Course

```bash
python to_html.py python-basics.md -o module1-quiz.html
```

### Create Test Without Shuffling

```bash
python to_html.py exam.md --no-shuffle-questions --no-shuffle-answers
```

### Create Quiz with Dark Theme

```bash
python to_html.py quiz.md --dark-mode -o dark-quiz.html
```

## Preview

Open the generated HTML file in a browser to see:

- **Light Theme** - clean, minimalist design
- **Dark Theme** - comfortable dark mode
- **Mobile Version** - adapted interface
- **Results Page** - detailed statistics

## License

This project is an interactive quiz generator for educational purposes.

## Author

Created with modern web technologies and Python best practices.

## Support

For questions and suggestions, create an issue in the project repository.

---

**Enjoy creating beautiful interactive quizzes!**
