# Goethe Booking Automation

Automated booking system for Goethe Institute exams with parallel session support and flexible module selection.

## 📁 Project Structure

```
automate/
├── main.py              # Main entry point - Configure profiles and accounts here
├── run_parallel.py      # Parallel booking manager utility
├── test.py              # Core booking bot implementation
└── README.md           # This file
```

## 🚀 Quick Start

1. **Configure your accounts in `main.py`**
2. **Run the booking**: `python main.py`

That's it!

## 📋 Files Overview

### `main.py` - Main Configuration
- **Purpose**: Define profiles, accounts, and run bookings
- **What to edit**: Add your accounts and assign profiles
- **Contains**:
  - `PROFILES`: Pre-defined module combinations
  - `get_accounts()`: Your account credentials and profile assignments
  - `get_shared_config()`: Common settings (URL, payment details, headless mode)

### `run_parallel.py` - Parallel Manager
- **Purpose**: Handles running multiple bookings simultaneously
- **What to edit**: Nothing! This is a utility module
- **Features**:
  - Parallel execution with asyncio
  - Individual logging per account
  - Success/failure tracking
  - Summary report

### `test.py` - Booking Bot
- **Purpose**: Core booking automation logic
- **What to edit**: Nothing unless you need to fix selectors
- **Handles**:
  - Cookie consent
  - City selection
  - Module selection with checkboxes
  - Login process
  - Payment handling

## 🎯 Usage Examples

### Example 1: Basic Setup (2 accounts)

```python
# In main.py -> get_accounts()

accounts = [
    {
        'email': 'user1@example.com',
        'password': 'pass123',
        'profile': 'reading_listening',
        'modules': PROFILES['reading_listening']['modules']
    },
    {
        'email': 'user2@example.com',
        'password': 'pass456',
        'profile': 'all_modules',
        'modules': PROFILES['all_modules']['modules']
    }
]
```

### Example 2: Many Accounts (5+ accounts)

```python
accounts = [
    {
        'email': 'user1@example.com',
        'password': 'pass1',
        'profile': 'reading_only',
        'modules': PROFILES['reading_only']['modules']
    },
    {
        'email': 'user2@example.com',
        'password': 'pass2',
        'profile': 'writing_speaking',
        'modules': PROFILES['writing_speaking']['modules']
    },
    {
        'email': 'user3@example.com',
        'password': 'pass3',
        'profile': 'listening_speaking',
        'modules': PROFILES['listening_speaking']['modules']
    },
    {
        'email': 'user4@example.com',
        'password': 'pass4',
        'profile': 'all_modules',
        'modules': PROFILES['all_modules']['modules']
    },
    {
        'email': 'user5@example.com',
        'password': 'pass5',
        'profile': 'speaking_only',
        'modules': PROFILES['speaking_only']['modules']
    }
]
```

### Example 3: Custom Module Combination

```python
# Add a custom profile in PROFILES
PROFILES['custom'] = {
    'name': 'My Custom Combo',
    'modules': ['reading', 'speaking']  # Any combination you want
}

# Use it in an account
{
    'email': 'custom@example.com',
    'password': 'pass',
    'profile': 'custom',
    'modules': PROFILES['custom']['modules']
}
```

## 📊 Available Profiles

| Profile Key | Modules | Description |
|------------|---------|-------------|
| `reading_listening` | Reading, Listening | Reading & Listening only |
| `writing_speaking` | Writing, Speaking | Writing & Speaking only |
| `all_modules` | All 4 | All modules |
| `reading_only` | Reading | Reading only |
| `listening_only` | Listening | Listening only |
| `writing_only` | Writing | Writing only |
| `speaking_only` | Speaking | Speaking only |
| `reading_writing` | Reading, Writing | Reading & Writing |
| `listening_speaking` | Listening, Speaking | Listening & Speaking |

## ⚙️ Configuration Options

### In `get_shared_config()`:

```python
{
    'start_url': 'https://www.goethe.de/...',  # Exam URL
    'card_details': {...},                      # Payment info (test card)
    'headless': False                          # True = no browser window
}
```

### Headless Mode
- `False`: Shows browser windows (for debugging)
- `True`: Runs in background (for production)

## 🏃 Running the Script

```bash
# Run with visible browsers (default)
python main.py

# To run in headless mode, set 'headless': True in get_shared_config()
```

## 📝 Output Example

```
================================================================================
BOOKING CONFIGURATION
================================================================================
Start URL: https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm
Total Accounts: 2
Headless Mode: False

Account 1: user1@example.com
  Profile: Reading & Listening Only
  Modules: Reading, Listening

Account 2: user2@example.com
  Profile: All Four Modules
  Modules: Reading, Listening, Writing, Speaking

================================================================================
[Account-1] - INFO - Starting booking session...
[Account-2] - INFO - Starting booking session...
...
================================================================================
BOOKING SUMMARY
================================================================================
✅ user1@example.com
   Status: SUCCESS
   Modules: Reading, Listening
   Duration: 45.23s

✅ user2@example.com
   Status: SUCCESS
   Modules: Reading, Listening, Writing, Speaking
   Duration: 52.67s

================================================================================
Total: 2 | Success: 2 | Failed: 0
================================================================================
```

## 🔧 Troubleshooting

### Issue: Script hangs or times out
- Check your internet connection
- Verify the `start_url` is correct
- Run in non-headless mode to see what's happening

### Issue: Checkbox selection not working
- The script uses JavaScript to click checkboxes
- If it fails, check if the website HTML has changed

### Issue: Login fails
- Verify email and password are correct
- Check if there's a CAPTCHA (not supported)

## 🎯 Adding More Accounts

Just add more dictionaries to the `accounts` list in `get_accounts()`:

```python
{
    'email': 'new@example.com',
    'password': 'newpass',
    'profile': 'all_modules',  # Choose any profile
    'modules': PROFILES['all_modules']['modules']
}
```

No limit on the number of accounts!

## ⚠️ Important Notes

1. **Parallel Execution**: All accounts run simultaneously
2. **Independent Sessions**: If one fails, others continue
3. **Test Card**: The default card number is for testing only
4. **Module Selection**: Uses JavaScript clicks to bypass UI issues
5. **Screenshots**: Error screenshots saved for debugging

## 📞 Support

If you encounter issues:
1. Check the error screenshots (e.g., `error_screenshot.png`)
2. Run in non-headless mode to see the browser
3. Check the console logs for specific errors
