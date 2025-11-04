# 🏔️ Wosland Bot - Quick Start Guide

## 🚀 Super Easy - Just Use State Number!

The bot now works **exactly like whiteoutsurvival.pl** - just enter your state number!

### ⚡ Instant Timeline (No Setup Required!)

```
!state 456
```

That's it! Get instant timeline for **any state number**:
- State456, State1234, State99, etc.
- Works immediately - no registration needed!

---

## 📝 Available Commands

### 🎯 Quick Commands (Recommended)

**`!state <number>`** - Instant timeline for any state
```
!state 456
!state State456
!state 1234
```
Shows: Age, Gen, SVS, Recent events, Upcoming events

**`!addstate <number>`** - Save a state for later
```
!addstate 456
```
Saves the state so you can use `!serverage State456`

---

### 📊 Saved States (Optional)

**`!serverage <name>`** - View saved state timeline
```
!serverage State456
```

**`!timeline <name>`** - Full detailed timeline
```
!timeline State456
```

**`!listservers`** - List all saved states
```
!listservers
```

**`!deleteserver <name>`** - Remove saved state
```
!deleteserver State456
```

---

### 🔧 Manual Setup (For Custom Dates)

**`!setserver <name> <date>`** - Set custom start date
```
!setserver MyState 2024-01-15
```
Use this if you know the exact launch date

**`!woshelp`** - Show help menu
```
!woshelp
```

---

## 💡 Most Common Usage

### Check Any State Instantly:
```
!state 456
```

### Save Your State:
```
!addstate 456
```

### Check It Later:
```
!serverage State456
```

---

## 📊 What You Get

Every timeline shows:

✅ **Server Age**: Days, weeks, season  
✅ **Hero Generation**: Current gen (1-13+)  
✅ **SVS Info**: Total events, next SVS date  
✅ **Next Major Unlock**: Countdown to next feature  
✅ **Recent Achievements**: Last 5 events unlocked  
✅ **Coming Soon**: Next 3 upcoming events  

---

## 🎮 Examples

### Check Your State:
```
!state 789
```
**Output:**
- 📊 125 days old, Season 2
- ⭐ Gen 3 Era
- ⚔️ 8 SVS events
- 🗓️ Next SVS: Nov 5 (3 days)
- 🎊 Next: War Academy in 95 days
- ✅ Recent: Gen 3 Heroes, Pets, Crystals
- 🔮 Coming: Legendary Gear, Gen 4

### Save Multiple States:
```
!addstate 456
!addstate 789
!addstate 1001
!listservers
```

### Full Timeline:
```
!timeline State456
```
Shows all hero gens, features, pets unlocked

---

## 🔥 Key Features

- **No Setup Required**: Just type state number!
- **Auto-Calculated**: Estimates server age from number
- **40+ Events Tracked**: Heroes, pets, features, major updates
- **SVS Predictions**: 14-day cycle tracking
- **Hero Generations**: Tracks Gen 1-13+
- **Smart Countdowns**: Days until next unlock

---

## 💬 Quick Tips

1. **Fastest way**: `!state <number>` - works instantly!
2. **Check any state**: Works for State1 to State9999+
3. **Save favorites**: Use `!addstate` for quick access
4. **Full timeline**: Use `!timeline` for complete view

---

## 📱 Bot Setup

1. **Install dependencies:**
   ```powershell
   .\start.bat
   ```

2. **Add bot token to `.env`**

3. **Run the bot:**
   ```powershell
   python bot.py
   ```

4. **Use it:**
   ```
   !state 456
   ```

---

**Made with ❄️ for the WOS community!**

Just type `!state <your_state_number>` and go! 🚀
