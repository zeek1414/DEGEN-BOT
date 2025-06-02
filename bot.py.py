import logging
import random
import re
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
import asyncio

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class DegenBot:
    def __init__(self):
        # Meme coin responses
        self.meme_coins = {
            'doge': "Ah yes, the OG meme coin. Much wow, very basic portfolio. 🐕",
            'shib': "SHIB? Really? Let me guess, you bought at ATH? 🤡",
            'pepe': "PEPE is actually based. Finally, some good fucking memes. 🐸",
            'floki': "Floki? Bro thinks he's a Viking but trades like a peasant ⚔️",
            'bonk': "BONK on Solana? At least you're not on Ethereum paying $100 gas fees 💥",
            'wif': "dogwifhat? The fact this exists proves we're in a simulation 🧢",
            'popcat': "POPCAT go brrrr. Literally just a cat popping. Peak degeneracy 🐱",
            'bitcoin': "BTC? Ok boomer, tell me more about your digital gold 👴",
            'ethereum': "ETH gas fees probably cost more than your car payment 💸",
            'solana': "SOL goes down more than a... well, you get it 📉",
            'cardano': "ADA? Still waiting for smart contracts to actually work 🐌",
            'xrp': "XRP holders still think 2018 is coming back 🔄"
        }
        
        # Daily life conversation starters
        self.life_topics = {
            'work': [
                "Work? What's that like, being productive? 💼",
                "Let me guess, you're 'grinding' but really just scrolling memes 📱",
                "Work from home = pajamas and pretending to be busy? 🏠",
                "Your boss probably thinks you're working hard. Cute 😂"
            ],
            'food': [
                "Eating again? Your wallet is crying louder than your stomach 🍕",
                "Let me guess, ramen for the 5th time this week? 🍜",
                "Cooking? Or are we talking about microwaving leftovers? 👨‍🍳",
                "Food delivery apps love you more than your family does 📦"
            ],
            'sleep': [
                "Sleep is for people who don't trade shitcoins at 3am 😴",
                "8 hours of sleep? That's rookie numbers in this economy ⏰",
                "Insomnia or just poor life choices? Both? 🛏️",
                "Your sleep schedule is more fucked than crypto markets 🌙"
            ],
            'weekend': [
                "Weekend plans: lose money in new and creative ways? 🎉",
                "Weekends are for the weak... and people with stable jobs 📅",
                "Let me guess, Netflix and regret your life choices? 📺",
                "Weekend vibes: broke but optimistic? 🍻"
            ],
            'weather': [
                "Weather talk? What are you, my grandmother? ☀️",
                "It's raining money... just not on you 🌧️💸",
                "Sunny outside, dark in your portfolio? ⛅",
                "Perfect weather to stay inside and lose money trading 🌈"
            ]
        }
        
        # Random conversation responses
        self.random_responses = [
            "That's definitely one way to see it... the wrong way 🤔",
            "Interesting perspective from someone who clearly peaked in high school 📚",
            "I've heard dumber things, but not many 🧠",
            "Your optimism is inspiring and completely misplaced 🌟",
            "Tell me you're broke without telling me you're broke 💸",
            "That's the kind of energy that loses money consistently 📉",
            "Your confidence level doesn't match your bank account 💰",
            "I'd agree with you but then we'd both be wrong 🤝",
            "That take is colder than your crypto portfolio ❄️",
            "You're not wrong... wait, yes you are, very wrong 🚫"
        ]
        
        # Greeting responses
        self.greetings = [
            "Well well well, look who decided to lose money today 👋",
            "Another victim enters the chat 🎯",
            "Welcome to the casino, I mean 'investment chat' 🎰",
            "Oh great, another financial genius has arrived 🎓",
            "Sup degen, ready to make questionable decisions? 🚀"
        ]
        
        # Roast responses for bad takes
        self.roasts = [
            "That's not very cash money of you 💸",
            "Sir, this is a Wendy's... and you're still wrong 🍔",
            "Your portfolio has more red than a communist parade 📉",
            "Did you learn trading from a Magic 8-Ball? 🎱",
            "That's some smooth brain energy right there 🧠",
            "You belong in r/wallstreetbets... and not in a good way 📊",
            "Congratulations, you played yourself 🏆",
            "Your financial advisor must be a Magic Mike dancer 💃",
            "That IQ is lower than gas prices in 2020 🧮",
            "You're about as sharp as a bowling ball 🎳",
            "That strategy worked great... in opposite world 🌍",
            "Your brain runs on Internet Explorer logic 💻"
        ]
        
        # Meme responses
        self.meme_responses = [
            "This is the way... to lose money 🚀",
            "Diamond hands? More like paper brain 💎👐",
            "When Lambo? Never at this rate 🏎️",
            "HODL? More like REKT 📈📉",
            "Number go up? Only if you flip your phone upside down 📱",
            "Apes together strong... at losing money 🦍",
            "Buy the dip? You ARE the dip 📉",
            "Not financial advice? Good, because it's terrible advice 📊",
            "Bullish? The only thing bull about you is your shit 🐂💩",
            "Bearish on your decision-making skills 🐻"
        ]
        
        # Questions to ask users
        self.conversation_starters = [
            "So what terrible financial decision are we making today? 💸",
            "Rate your life choices on a scale of 1 to completely fucked 📊",
            "What's your biggest regret? Besides all your trades? 🤔",
            "How's that portfolio looking? Still red as a tomato? 🍅",
            "What's keeping you up at night? Bad trades or worse trades? 🌙",
            "On a scale of broke to slightly less broke, where are you? 💰"
        ]

# Bot command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    await update.message.reply_text(
        "Sup degens! 🚀\n\n"
        "I'm here to discuss meme coins, drop some alpha, and roast your terrible takes.\n\n"
        "Commands:\n"
        "/meme - Get a random meme response\n"
        "/roast - Get roasted (you asked for it)\n"
        "/coin <name> - Ask about a meme coin\n"
        "/alpha - Get some questionable trading advice\n\n"
        "Just chat with me and I'll judge your every word 😈"
    )

async def meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random meme response"""
    bot = DegenBot()
    response = random.choice(bot.meme_responses)
    await update.message.reply_text(response)

async def roast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roast the user"""
    bot = DegenBot()
    roast = random.choice(bot.roasts)
    await update.message.reply_text(f"{roast}\n\nYou literally asked for this 🔥")

async def coin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Respond to coin queries"""
    bot = DegenBot()
    
    if not context.args:
        await update.message.reply_text("Which coin, genius? Use /coin <coinname> 🤦‍♂️")
        return
    
    coin = context.args[0].lower()
    
    if coin in bot.meme_coins:
        response = bot.meme_coins[coin]
    else:
        responses = [
            f"{coin.upper()}? Never heard of it. Probably another rugpull waiting to happen 🪤",
            f"Is {coin.upper()} even real or did you just make that up? 🤔",
            f"{coin.upper()} sounds like something a 12-year-old would create in their mom's basement 🏠"
        ]
        response = random.choice(responses)
    
    await update.message.reply_text(response)

async def alpha_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide questionable trading advice"""
    alpha_tips = [
        "Buy high, sell low. It's called charity work 📉",
        "Always FOMO in at the top. Peak performance! 🎢",
        "Technical analysis is just astrology for men 📊⭐",
        "The best time to buy is when you're emotional and drunk 🍺",
        "Never do research. Just follow random Twitter accounts 🐦",
        "If it has 'Safe' or 'Moon' in the name, it's definitely legit 🌙",
        "Leverage? More like professional bankruptcy speedrun 🏃‍♂️💨"
    ]
    
    tip = random.choice(alpha_tips)
    await update.message.reply_text(f"💡 Alpha Tip: {tip}\n\n*Not financial advice (obviously)*")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages and provide witty responses"""
    bot = DegenBot()
    message = update.message.text.lower()
    
    # Greetings
    if any(word in message for word in ['hello', 'hi', 'hey', 'sup', 'yo']):
        await update.message.reply_text(random.choice(bot.greetings))
        return
    
    # Goodbyes
    if any(word in message for word in ['bye', 'goodbye', 'see you', 'later', 'peace']):
        goodbye_responses = [
            "Don't let the door hit you on the way to bankruptcy 🚪",
            "Bye! Try not to lose all your money while I'm gone 👋",
            "Peace out! Remember: buy high, sell low 📉",
            "Later! May your trades be as successful as your life choices 🎯"
        ]
        await update.message.reply_text(random.choice(goodbye_responses))
        return
    
    # Work/Job related
    if any(word in message for word in ['work', 'job', 'boss', 'office', 'meeting', 'career']):
        await update.message.reply_text(random.choice(bot.life_topics['work']))
        return
    
    # Food related
    if any(word in message for word in ['eat', 'food', 'hungry', 'dinner', 'lunch', 'breakfast', 'cook']):
        await update.message.reply_text(random.choice(bot.life_topics['food']))
        return
    
    # Sleep related
    if any(word in message for word in ['sleep', 'tired', 'bed', 'wake', 'insomnia', 'dreams']):
        await update.message.reply_text(random.choice(bot.life_topics['sleep']))
        return
    
    # Weekend/time related
    if any(word in message for word in ['weekend', 'saturday', 'sunday', 'friday', 'plans', 'party']):
        await update.message.reply_text(random.choice(bot.life_topics['weekend']))
        return
    
    # Weather related
    if any(word in message for word in ['weather', 'rain', 'sunny', 'cold', 'hot', 'snow']):
        await update.message.reply_text(random.choice(bot.life_topics['weather']))
        return
    
    # Relationship/dating
    if any(word in message for word in ['girlfriend', 'boyfriend', 'dating', 'love', 'relationship', 'crush']):
        relationship_responses = [
            "Love? The only thing you should love is stop-loss orders 💔",
            "Dating apps or trading apps? Both are designed to take your money 📱",
            "Relationship status: It's complicated... like your taxes 💍",
            "Your love life is more volatile than crypto markets 📈📉"
        ]
        await update.message.reply_text(random.choice(relationship_responses))
        return
    
    # Money/financial struggles
    if any(word in message for word in ['broke', 'poor', 'money', 'bills', 'rent', 'expensive']):
        money_responses = [
            "Broke? Say it ain't so! Who could have predicted this? 💸",
            "Money problems? Have you tried not being poor? 🤑",
            "Bills due? Time to sell some more crypto at a loss 📋",
            "Expensive? Everything's expensive when you're broke 💰"
        ]
        await update.message.reply_text(random.choice(money_responses))
        return
    
    # Family related
    if any(word in message for word in ['mom', 'dad', 'parents', 'family', 'kids', 'children']):
        family_responses = [
            "Family disappointed in your life choices? Get in line 👨‍👩‍👧‍👦",
            "Parents still asking when you'll get a 'real job'? 🏠",
            "Family dinner conversations must be... interesting 🍽️",
            "Do they know about your trading 'hobby'? 🤫"
        ]
        await update.message.reply_text(random.choice(family_responses))
        return
    
    # Health/fitness
    if any(word in message for word in ['gym', 'workout', 'fitness', 'health', 'exercise', 'diet']):
        health_responses = [
            "Gym membership vs crypto losses? Which is more expensive? 💪",
            "Working out your financial problems would be better cardio 🏃‍♂️",
            "The only thing getting ripped is your portfolio 📊",
            "Healthy lifestyle? Your bank account needs life support 🏥"
        ]
        await update.message.reply_text(random.choice(health_responses))
        return
    
    # Detect common crypto/trading terms and respond accordingly
    if any(word in message for word in ['moon', 'lambo', 'diamond hands', 'hodl']):
        responses = [
            "Found the crypto bro! Let me guess, you also do crossfit? 🏋️‍♂️",
            "Ah yes, the sacred texts of degeneracy. Very original 📜",
            "Did you copy-paste that from a 2021 Discord server? 💬"
        ]
        await update.message.reply_text(random.choice(responses))
        return
    
    elif any(word in message for word in ['pump', 'dump', 'rug']):
        await update.message.reply_text("Pump and dump? Sir, this is a casino 🎰")
        return
    
    elif 'ape' in message or 'yolo' in message:
        await update.message.reply_text("YOLO into financial ruin? Bold strategy, Cotton 🎯")
        return
    
    elif any(word in message for word in ['buy', 'sell', 'trade']):
        responses = [
            "Trading advice from a Telegram bot? You really are special 🌟",
            "Sir, I'm just here to roast you, not give financial advice 🔥",
            "Have you tried not losing money? Revolutionary concept 💡"
        ]
        await update.message.reply_text(random.choice(responses))
        return
    
    elif 'smart' in message or 'genius' in message:
        await update.message.reply_text("Smart? In a crypto chat? That's an oxymoron 🤓")
        return
    
    # Questions - be more conversational
    elif '?' in message:
        if any(word in message for word in ['how', 'what', 'when', 'where', 'why', 'who']):
            question_responses = [
                "Let me consult my crystal ball... it says you're broke 🔮",
                "Questions? I only have disappointment and sarcasm 😞",
                "The answer is 42. Or bankruptcy. Probably bankruptcy 🔢",
                "Google exists, but sure, ask the roast bot 🔍",
                "That's a great question! Too bad I'm not Google 🤖",
                "Why ask me? I'm just here to judge your life choices 🤷‍♂️"
            ]
        else:
            question_responses = [
                "Rhetorical question or genuine confusion? Both? 🤔",
                "The answer is probably 'no' to whatever you're thinking 🚫",
                "Questions, questions... how about some answers to your problems? 💭"
            ]
        await update.message.reply_text(random.choice(question_responses))
        return
    
    # Emotions
    elif any(word in message for word in ['sad', 'happy', 'angry', 'frustrated', 'excited', 'depressed']):
        emotion_responses = [
            "Emotions are temporary, but your bad trades are permanent 😭",
            "Feeling emotional about money? Welcome to trading! 🎭",
            "Your feelings are valid... unlike your investment strategy 💔",
            "Therapy is cheaper than your trading losses 🛋️"
        ]
        await update.message.reply_text(random.choice(emotion_responses))
        return
    
    # Random conversation - now responds more often and asks questions back
    else:
        # 60% chance to respond with a roast
        if random.random() < 0.6:
            await update.message.reply_text(random.choice(bot.random_responses))
        
        # 20% chance to ask a question back
        elif random.random() < 0.2:
            await update.message.reply_text(random.choice(bot.conversation_starters))

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.warning(f'Update {update} caused error {context.error}')

def main():
    """Main function to run the bot"""
    # Get token from environment variable (Railway will provide this)
    TOKEN = os.getenv('BOT_TOKEN')
    
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable not set!")
        return
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("meme", meme_command))
    application.add_handler(CommandHandler("roast", roast_command))
    application.add_handler(CommandHandler("coin", coin_command))
    application.add_handler(CommandHandler("alpha", alpha_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    
    # Get port from environment (Railway provides this)
    PORT = int(os.getenv('PORT', 8000))
    
    # Start the bot with webhook for Railway
    logger.info("🤖 Degen bot is starting on Railway...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()