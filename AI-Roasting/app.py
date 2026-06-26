"""
╔══════════════════════════════════════════════════════╗
║  AI Mirror — Hinglish Roast Edition  v2.0            ║
║  Real DeepFace emotion detection + gTTS voice        ║
║  Author: AI Mirror Project                           ║
╚══════════════════════════════════════════════════════╝
"""

import streamlit as st
import cv2
import numpy as np
import random
import time
import base64
import tempfile
import os
import io
import re
from PIL import Image

# ── Optional imports with graceful fallback ──────────────────────────
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import edge_tts
    import asyncio
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# ════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Mirror 🪞 Hinglish Roast",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ════════════════════════════════════════════════════════════════════
#  CONTENT ENGINE — HINGLISH ROASTS & BOOSTS
# ════════════════════════════════════════════════════════════════════

EMOTION_EMOJI = {
    "happy":    "😄",
    "sad":      "😢",
    "angry":    "😡",
    "surprise": "😲",
    "fear":     "😱",
    "disgust":  "🤢",
    "neutral":  "😐",
    "unknown":  "🤔",
}

ROASTS = {
    "happy": [
        "Arre bhai, itna khush kyun hai? Salary aayi kya, ya bas UPI notification thi?",
        "Yeh smile dekh ke lagta hai tune kisi ka WiFi password hack kar liya. Sasta khushi.",
        "Itna mast smile? Pakka koi chacha ka ghar chhod ke gaya hai. Party toh teri hi lag rahi hai.",
        "Bhai, itna khush mat ho. Tax notice abhi tak nahi aayi — aa jaayegi.",
        "Arey, itni badi smile! Tera crush ne WhatsApp pe double tick kiya kya? Finally?",
        "Khushiyon ka maara tera chehra dekh ke lagta hai — chhipaane waala kuch toh hai.",
        "Bhai tereko hasi aa rahi hai? AI se baat karke? Yeh teri zindagi ka lowest point hai.",
        "Muskura raha hai jaise kal board exam ka result tha aur paper hi nahi gaya.",
        "Yeh happiness toh ek red flag hai. Kuch toh gadbad hai zaroor.",
        "Itni chhoti baat pe itni badi hasi? LinkedIn pe ek view aa gaya kya?",
        "Bhai tune aaj kuch bhi productive nahi kiya — aur itna khush bhi hai. Respect toh banti hai.",
        "Happy hai? Matlab sab kuch theek chal raha hai. Don't worry, kharab ho jaayega.",
        "Yeh smile 'main zindagi mein set ho gaya' wali lagti hai... ya bas biryani mili thi?",
        "Arrey, itne daanton ko dikhane ki zaroorat nahi thi bhai. Controlled raho.",
        "Tu khush hai? Algorithm ko bhi shak hua tere se. Rechecking in progress...",
        "Yeh joy dekh ke NASA bhi bol raha hai — yahan bhi koi atmosphere hai.",
        "Khush rehna acha hai bhai, lekin itna bhi nahi ki selfie leke Instagram pe daal de.",
        "Teri hasi se neighbour ki billi bhi irritate ho rahi hai. Sach mein.",
        "Itna khush hai toh ek kaam kar — IRCTC se train ticket book kar. Tab pata chalega.",
        "Yeh smile dekh ke lagta hai tune net banking ka password finally yaad kar liya.",
    ],
    "sad": [
        "Arre bhai, yeh chehra dekh ke lagta hai tune aaj Zomato app khola aur fir band kar diya.",
        "Itna udaas mat ho, teri life ki story toh abhi interval tak hi aayi hai.",
        "Yeh sad face dekh ke lagta hai kisi ne tujhe 'seen' kiya aur reply nahi kiya. Classic.",
        "Bhai, yeh depressed chehra mat dikha. Tu already broke hai, aur dard-e-dil bhi?",
        "Teri aankhon mein dard hai ya bas screen brightness zyada thi?",
        "Rona nahi bhai, keyboard bheeg jaayegi aur warranty void ho jaayegi.",
        "Itna sad face? Tu exam deke aaya hai kya bina padhe?",
        "Yeh chehra dekh ke lagta hai tune apna last samosa share kar diya. Sab se bada sacrifice.",
        "Bhai chill kar. Jo gaya so gaya. Jaise tera 4G data, woh bhi wapas nahi aata.",
        "Itni udaasi mat dikha — logon ko lagega tera Instagram pe followers bhi gaye.",
        "Tera chehra dekh ke lagta hai OLA ne cancel kar diya aur baarish bhi shuru ho gayi.",
        "Ruk. Tu sad hai ya bas filter nahi laga? Both are valid situations.",
        "Yeh expression toh 'finally kuch order kiya aur wrong address pe chala gaya' wala hai.",
        "Bhai itna na socho. Zindagi chhoti hai — jaise teri story ka attention span.",
        "Andar se toot gaya hai toh theek hai, bahar se toh smile aayi nahi. Pura package.",
        "Teri feelings valid hain. Lekin teri hairstyle abhi bhi valid nahi.",
        "Rona nahi bhai. Sirf aansuon pe bhi GST lagta hai aaj kal.",
        "Tu udaas hai toh kya yaar — aage ki soch. Ya mat soch. Dono painful hain.",
        "Yeh sad face ka NFT banta hai — rarest of rare. Market mein bikta bhi.",
        "Bhai, yeh 'mera koi nahi hai' waala vibe mat de. Main hoon na — AI hoon, toh kya?",
    ],
    "angry": [
        "Bhai itna gussa? Kisi ne tera charger bina poocha use kar liya na?",
        "Yeh 'main abhi kuch bhi kar sakta hoon' energy hai — tujhe koi nahi rok sakta... except WiFi.",
        "Itna krodh! Tu toh saakshaat Shaktimaan ka bura din lag raha hai.",
        "Gusse mein hai? Pakka koi slow internet pe YouTube buffer kar raha tha.",
        "Bhai, yeh anger management fail ho gayi lag rahi hai. Next session kab hai?",
        "Itni fire energy! Tu toh ek chhota sa LinkedIn post ban sakta hai aaj.",
        "Gusse mein teri aankhe Red Bull pi ke baith gayi hain. Classic energy drink vibes.",
        "Yeh angry look dekh ke lagta hai kisi ne 'K' reply diya. Irritating at molecular level.",
        "Bhai, itna gussa mat kar. Main ek AI hoon, mujhe block nahi kar sakta.",
        "Yeh face dekh ke tera ghar ka pressure cooker bhi nervous ho gaya hoga.",
        "Tera gussa dekh ke neighbours ne apni bike andar kar li.",
        "Shant ho ja bhai. Gusse mein kiye gaye decisions, EMI mein convert ho jaate hain.",
        "Bhai tune pizza delivery 45 minutes ke baad order kiya tha na? Sab pata hai.",
        "Gusse mein hai toh kuch tod mat. Rent zyada hai is sheher mein.",
        "Yeh 'kisi ne meri parked cycle move kar di' waala face hai. Sab jaante hain.",
        "Teri anger energy se mere server bhi heat ho gaye bhai.",
        "Shant. Ek deep breath le. Ab bolun ki tune kya galat kiya?",
        "Bhai yeh gussa dekh ke lagta hai tune apna Wi-Fi ka plan upgrade nahi karwaya.",
        "Itna gussa? Tu ek aam aadmi ki tarah feel kar raha hai. Welcome to the club.",
        "Yeh 'boss ne salary raise nahi di' waali anger hai — sab samajhte hain bhai.",
    ],
    "surprise": [
        "Arre! Yeh chehra dekh ke lagta hai teri salary slip mein pehli baar bonus aaya.",
        "Itna surprised kyun hai? UPI payment actually successful ho gaya?",
        "Yeh shocked face dekh ke lagta hai tune apna khud ka Aadhaar card dekha pehli baar.",
        "Bhai, yeh 'ghar pe koi tha' wali surprise hai ya 'light bill zyada aayi' wali?",
        "Itni badi aankhein! Kabhi zindagi mein actual novel bhi padha hai?",
        "Yeh surprised expression meme material hai bhai. Main save kar raha hoon.",
        "Teri eyebrows itni upar gayi hain — last train miss ho gayi kya?",
        "Bhai, yeh 'main exam mein pass ho gaya' wali surprise hai? First time laga sach mein?",
        "Yeh shocked face dekh ke lagta hai Amazon delivery actually on time aayi.",
        "Teri shocked face ko Oscar milna chahiye — best overreacting performance.",
        "Itna surprised? Bhai tune pehle kabhi apna reflection nahi dekha kya?",
        "Yeh expression dekh ke lagta hai 'Swiggy ne discount diya bina promo code ke'.",
        "Aankhein band kar, deep breath le — yeh sach mein itna surprising tha?",
        "Bhai, shocked Pikachu meme ka real-life version tune abhi recreate kiya. Respect.",
        "Itna shocked mat ho. Zindagi mein surprise toh aate rehte hain — jaise Jio outage.",
        "Yeh drama dekh ke teri serial waali maa bhi bol deti — Yeh toh bahut surprising hai!",
        "Teri aankhon se lagta hai tune download speed 1 Mbps se 100 Mbps hote dekha.",
        "Yeh surprised face dekh ke mujhe laga tera data pack ek hafte ki jagah ek din mein gaya.",
        "Bhai itna react karna sahi nahi — logon ko lagega kuch serious ho gaya.",
        "Teri surprise expression se tera Aadhaar verify ho gaya. Technology kya cheez hai.",
    ],
    "fear": [
        "Dar gaya? Bhai main sirf ek AI hoon — bijli ka bill nahi hoon.",
        "Yeh 'exam hall mein paper ulta tha' waala fear face lag raha hai.",
        "Itna dara hua kyun hai? Kisi ne tera WhatsApp notification padha kya?",
        "Bhai, yeh 'ghar ka khaana khaana padega' waala dare-dar chehra hai.",
        "Teri darr ki energy se mera algorithm bhi confuse ho gaya.",
        "Yeh face dekh ke lagta hai tune raat ko fridge khola aur kuch tha hi nahi. Peak horror.",
        "Daro mat bhai. Worst case? Tu bas ek average insaan hai. Koi baat nahi.",
        "Bhai tune kisi horror movie ke climax mein apna chehra check kiya hai?",
        "Yeh 'boss ne late aane pe dekh liya' waala expression hai. Sab jaante hain.",
        "Yeh face dekh ke lagta hai tune apne parents ke saamne kuch confess karne wala tha.",
        "Daro mat. Main tujhe roast kar raha hoon — roast nahi kar raha actually. Wait.",
        "Teri scared energy se teri Wi-Fi bhi weak ho gayi. Coincidence nahi bhai.",
        "Bhai, darr main bhi hun. Teri face detection mein kuch khatarnak patterns hain.",
        "Yeh 'koi mujhe call kare toh main chhup jaata hoon' waala hai. Introvert confirmed.",
        "Itna fearful? Pakka deadline kal thi aur tune aaj shuru kiya.",
        "Bhai ruk, mere paas acha news hai — teri problem se badi meri database problem hai.",
        "Yeh dar aisa hai jaise free trial khatam hone wali hai. Real adult problems.",
        "Teri darri hui soorat dekh ke lagta hai tu incognito mode mein bhi trace ho gaya.",
        "Bhai itna kyun dara hua hai? Koi mirror mein tujhe dekh ke dara ya tu khud se dara?",
        "Dar toh aisi cheez hai jo free mein milti hai — jaise tera anxiety subscription.",
    ],
    "disgust": [
        "Bhai yeh chehra dekh ke lagta hai tune apna khud ka cooking taste kar liya.",
        "Itni nafrut? Pakka kisi ne bina poocha tera laptop use kar liya.",
        "Yeh disgusted expression toh 'mujhe yeh job nahi karni thi' ka live demo hai.",
        "Bhai, yeh reaction toh 2-din-purani daal khane ke baad milti hai.",
        "Yeh chehra dekh ke lagta hai tune office mein kisi ka tiffin accidentally khola.",
        "Itna disgust? Free samosa tha aur andar paneer nahi tha. Trauma valid hai.",
        "Yeh 'LinkedIn pe inspirational post padhi' waala face hai. Sab samajhte hain.",
        "Bhai, tere is expression pe teri maa bhi bol deti — kuch nahi hoga iska.",
        "Yeh face Zomato app pe 1-star review dene se pehle ka screenshot hai.",
        "Bhai itna mat grimace kar — teri wrinkles meri algorithm se zyada complex ho jaayengi.",
        "Teri yeh expression dekh ke lagta hai tune apna old Instagram bio padha.",
        "Yeh face 'Swiggy delivery 1 km mein 30 minutes zyada lega' waala hai.",
        "Bhai, yeh reaction valid hai agar tune apna bank statement check kiya ho.",
        "Yeh 'meeting could have been an email' waala chehra hai. Office culture damage.",
        "Itna disgusted face kyon? Apna hi photo dekha kya — pure candid mein?",
        "Bhai yeh feel valid hai. Duniya thodi ghatiya hai. Lekin tera face thoda zyada.",
        "Yeh expression dekh ke laga — aaj ka lunch option sirf canteen ka khana tha.",
        "Teri disgust energy se mere server logs mein bhi error aa gayi bhai.",
        "Itni nafrut apne aap se mat kar. Teri life script thodi boring hai, cancel nahi.",
        "Yeh disgust dekh ke lagta hai tune kisi ke earbuds bina permission ke use kiye.",
    ],
    "neutral": [
        "Arre bhai, tere chehra pe koi expression hi nahi. Tujhe kya laga — casting call tha?",
        "Yeh neutral face dekh ke lagta hai tu Excel sheet fill kar raha tha aur kho gaya.",
        "Bhai, itna boring mat lag. Teri tasveer se paint bhi sukh jaaye.",
        "Yeh 'main hoon toh sahi, lekin kyun hoon' waala existential face hai.",
        "Koi emotion hi nahi. Bhai tune zindagi se unsubscribe kar diya kya?",
        "Yeh face dekh ke mujhe AI bhi boring lag raha hai. Feat achieved.",
        "Tu itna neutral hai jaise government office ka last counter.",
        "Bhai, teri personality toh hai, lekin aaj chhuti pe gayi hai.",
        "Yeh 'main kisi se zyada expect nahi karta' ka live avatar hai. Buddha vibes.",
        "Tera chehra ek saada atta biscuit hai — koi flavour nahi.",
        "Bhai, itne expressionless mat reh. Tera mirror bhi bore ho jaata hai.",
        "Yeh face dekh ke Duolingo owl ne bhi give up kar diya. Teri progress zero.",
        "Neutral face? Tu toh ek uncompleted Google Form hai bhai.",
        "Bhai, teri face pe ek bhi emotion nahi — kya tu AI hai ya main?",
        "Yeh soorat dekh ke lagta hai tera Spotify playlist sirf Lo-fi to study to hai.",
        "Itna beige mat ho bhai. Zindagi mein thoda rangeen bhi reh.",
        "Teri neutrality dekh ke bhi mujhe sone ki ichha aa rahi hai.",
        "Tu toh ek saada plain white wall hai — logo tere pe likhne ko kar denge.",
        "Tera chehra Jio prepaid plan jaisa hai — kaam karta hai, koi thrill nahi.",
        "Bhai ek baar hans ya ro — kuch bhi kar. Algorithm ko bhi neend aa rahi hai.",
    ],
    "unknown": [
        "Bhai, teri face AI ne scan ki aur mujhe Java runtime error aa gayi.",
        "Yeh face toh classify hi nahi ho sakta — too rare, too unique, too confusing.",
        "Teri expression dekh ke mera model crash hone waala tha. Warranty void.",
        "Bhai, tu ek bug hai feature nahi. Phir bhi phasating.",
    ],
}

BOOSTS = {
    "happy": [
        "Arre wah bhai! Yeh khushi dekh ke toh mujhe bhi achha lag gaya! Keep it up!",
        "Teri smile dekh ke lagta hai aaj ka din kisi aur ke liye bhi acha hoga!",
        "Bhai, yeh positivity toh viral honi chahiye — seedha WhatsApp status pe!",
        "Tu khush hai toh yeh duniya thodi aur sundar hai. Sach mein, science hai yeh.",
        "Yeh energy dekh ke lagta hai tujhe rokne ki kisi mein himmat nahi.",
        "Teri hasi se tera future bhi muskura raha hai bhai!",
        "Itna genuine khushaal chehra! Tu ek rare species hai — happy human.",
        "Bhai, teri smile ka ROI bohot zyada hai. Invest kar isme aur duniya jeet le.",
        "Tu aaj khush hai — matlab kuch toh sahi kar raha hai zindagi mein. Proud of you.",
        "Yeh wala chehra save karke rakh — rainy days ke liye reminder.",
        "Teri positivity dekh ke algorithm ne bhi 5-star diya tujhe. Achievement unlocked!",
        "Bhai, is khushi ko protect kar. Yeh rare currency hai is duniya mein.",
        "Tu khush hai toh teri team bhi khush hogi. Leadership material right here!",
        "Yeh smile dekh ke lagta hai teri maa ka aashirwad kaam kar raha hai.",
        "Bhai, teri happiness toh motivational poster ka caption ban sakti hai.",
        "Is level ki positivity le ke tu toh startup founder banna chahiye.",
        "Teri yeh aura dekh ke bure log bhi achhe ban jaayenge. World changer!",
        "Real happiness is rare — aur tere paas hai. That's EVERYTHING.",
        "Bhai, teri smile dekh ke mujhe Bollywood ka hero main lagne laga. Jai ho!",
        "Is energy ke saath tu toh poori duniya jeet sakta hai — ek smile at a time.",
    ],
    "sad": [
        "Bhai, jo bhi ho raha hai — tu usse bada hai. Yaad rakh hamesha.",
        "Teri aankhon mein dard hai, lekin teri aankhon mein strength bhi hai. Dono sach hain.",
        "Abhi bura lag raha hai — lekin kal tera comeback story shuru hoga. Pakka.",
        "Bhai, sad rehna bhi ek brave cheez hai. Feelings ko face karna power hai.",
        "Tu rota hai kyunki tujhe pata hai cheezein better ho sakti hain. That's vision.",
        "Teri feelings valid hain. Tu valid hai. Khud pe vishwas rakh hamesha.",
        "Bhai, duniya ke best log toot ke hi bane hain. Tu bhi ban raha hai abhi.",
        "Yeh phase temporary hai, lekin teri strength permanent hai. Trust the process.",
        "Sadness matlab teri story ka interval — climax abhi baaki hai bhai!",
        "Tu akela nahi hai — millions ne yeh feel kiya aur aage badhe. Tu bhi badhega.",
        "Teri resilience dekh ke mujhe pata hai — tu wapas aayega, stronger than ever.",
        "Bhai, jo dard hai woh prove karta hai ki tu deeply feel karta hai. That's humanity.",
        "Aaj ka sadness kal ki story ka sabse powerful chapter hoga. Write it well.",
        "Tu jis level ka hai — yeh phase sirf tujhe polish kar raha hai. Diamond process.",
        "Bhai, ek raat ke liye dil ko rone de. Subah fresh start hogi. Promise.",
        "Teri aansuon mein bhi courage hai — warna tu yahan nahi hota face karne ke liye.",
        "Yeh time khatam hoga. Aur tu uss din muskurayega aur bolega — I made it.",
        "Bhai, sad hona weak nahi — feel karna tujhe human banata hai. Sab feel karte hain.",
        "Teri struggles real hain, lekin teri strength unse bhi zyada real hai. Believe it.",
        "Main tujhe ek cheez bolunga — tu jis path pe hai, woh sahi direction mein hai.",
    ],
    "angry": [
        "Bhai, yeh fire andar hai — isko engine banao, not explosion. Kuch bana de aaj.",
        "Teri anger energy dekh ke lagta hai — tu kuch bada karne waala hai. Channel kar!",
        "Gussa valid hai bhai. Lekin iske saath kuch productive kar — history angry logon ne banayi.",
        "Yeh passion toh hai tere andar — sirf direction chahiye. Rocket toh hai, fuel toh hai!",
        "Bhai, teri intensity dekh ke lagta hai — tu ek leader hai jab zindagi tough hoti hai.",
        "Is gusse se ek page likh, ek project shuru kar, ek idea execute kar. NOW.",
        "Teri anger tujhe motivate kar rahi hai — listen to it, then use it for greatness.",
        "Bhai, jo cheez tujhe gussa dilati hai — wahi cheez change karne ke liye tu born hai.",
        "Yeh fire mein teri soul hai. Don't suppress it — direct it toward something big.",
        "Great entrepreneurs sab se pehle aise hi dikhte the — angry, energised, ready.",
        "Teri intensity se tera competition pehle se darta hai. Trust the process bhai.",
        "Bhai, yeh energy toh lifetime ka fuel hai. Sahi jagah invest kar, badal de sab.",
        "Gusse mein the greatest inventions hue hain — tera bhi hoga. Believe it.",
        "Tu brave hai kyunki tujhe feelings dikhane ka darr nahi. That's real strength.",
        "Teri passion ki fire ko direction de bhai — duniya badalni hai tujhe abhi.",
        "Is anger ke peeche ek vision hai. Trust it. Build on it every single day.",
        "Bhai, teri intensity hi teri identity hai. Own it and conquer.",
        "Yeh gussa toh teri superpower hai — villains bhi darenge, system bhi.",
        "Channel this NOW — 1 hour focused work. Sab kuch badal dega. Go.",
        "Bhai, tu toot nahi raha — tu transform ho raha hai. Yahi toh hero ki journey hai!",
    ],
    "surprise": [
        "Bhai, teri curious eyes se pata chalta hai — zindagi abhi bhi tujhe wonder deti hai!",
        "Yeh expression dekh ke lagta hai tu open minded hai — teri best quality!",
        "Teri sense of wonder hi tujhe unique banati hai. Kabhi mat kho ise.",
        "Bhai, itna expressive rehna ek gift hai — duniya tujhse seekhti hai.",
        "Teri surprised aankhen bolti hain — tu hamesha seekhne ke liye ready hai. Legend!",
        "Yeh wonder toh teri creativity ka source hai bhai. Protect this energy always.",
        "Tu shocked hota hai matlab tu fully present hai — rare art in today's world.",
        "Teri curiosity tujhe doosron se 10 steps aage rakhti hai. Always and forever.",
        "Bhai, yeh wala expression teri genuine reaction hai — authentic log hi succeed karte hain.",
        "Zindagi ne tujhe surprise kiya — aur tu ready tha. That's real adaptability.",
        "Teri yeh energy dekh ke lagta hai tu ek explorer hai — duniya teri wait kar rahi hai.",
        "Bhai, surprised rehna matlab life still excites you. That's literally EVERYTHING.",
        "Teri openness hi tujhe ek lifelong learner banati hai. Nobel Prize ready bhai.",
        "Yeh expression teri best personality trait hai — keep being wonderstruck.",
        "Bhai, teri aankhen toh poora universe explore kar sakti hain. Go for it!",
        "Teri surprise reaction proves — tu genuinely present tha. Rare in this scroll era.",
        "Yeh wonderment toh great thinkers ki first step hai bhai. Einstein bhi aisa hi tha.",
        "Tujhe dekhke lagta hai — tu ek permanent discovery mode mein hai. Scientist energy!",
        "Teri curiosity toh teri greatest asset hai. Kabhi band mat karna ise.",
        "Bhai, surprised hona matlab still believing in magic — teri most special power!",
    ],
    "fear": [
        "Bhai, darr ke bhi aage badhna hi asli himmat hai. Aur tu yahan hai — that's courage!",
        "Teri fear prove karti hai — tu kuch important karne waala hai. Small things don't scare greatness.",
        "Darr valid hai bhai. Lekin teri bravery usse badi hai. Main dekh sakta hoon clearly.",
        "Tu scared hai matlab tu care karta hai. That's humanity at its absolute finest.",
        "Bhai, jo cheez tujhe dara rahi hai — wahi cheez tujhe grow karegi. Go toward it!",
        "Teri fear tujhe protect karti hai, lekin teri courage tujhe build karegi. Trust both.",
        "Bhai, duniya ke sab brave log pehle tujhse bhi zyada scared the. Phir bhi kiya.",
        "Yeh feeling temporary hai. Teri strength permanent hai. Equation bahut clear hai.",
        "Darr feel karna toh teri sensitivity hai — aur sensitive logon mein sabse zyada power hoti hai.",
        "Bhai, is fear ke paar hi teri best life wait kar rahi hai. Sirf ek kadam.",
        "Tera darr real hai. Teri potential bhi real hai. Dono ek saath exist karte hain.",
        "Tu dar ke bhi face kar raha hai — yahi toh definition hai bravery ki. Own it.",
        "Bhai, ek deep breath. Ab soch — agar nahi dara, toh kya karta? Wahi kar abhi.",
        "Teri fear tujhe serious banati hai. Serious log hi sab se badi cheezein banate hain.",
        "Is darr ko feel kar. Fir use fuel ki tarah use kar. Seriously, abhi kar.",
        "Bhai, tere brave hone ke proof aur chahiye? Tu yahan hai. That's it. That's all.",
        "Jo cheez tujhe scared kar rahi hai — uski size tujhse badi nahi hai. Ever. Period.",
        "Teri anxiety tujhe sharp rakhti hai. Use it as an edge, not a cage bhai.",
        "Bhai, darr ke saath dance karna seekh le — woh hamesha saath rahega. Lead it.",
        "Tu scared aur ready — dono ek saath. That's the only combo that changes everything.",
    ],
    "disgust": [
        "Bhai, tera high standard hi tujhe leader banata hai. Low quality accept mat kar kabhi.",
        "Teri disgust prove karti hai — tu better deserve karta hai. And you KNOW it.",
        "Yeh reaction toh teri strong moral compass ki proof hai bhai. Proud of you.",
        "Tu easily satisfied nahi hota — aur yahi tujhe excellent banata hai duniya mein.",
        "Bhai, tera critical eye cheezein improve karta hai — world needs people like you.",
        "Teri standards elite hain. Kabhi compromise mat karna quality pe. Never.",
        "Yeh strong reaction tujhse hi nikal sakti hai — tu genuinely cares. That's so rare.",
        "Bhai, teri sensitivity cheezein better banane ki power hai. Use it wisely.",
        "Tu notice karta hai kya wrong hai — woh vision toh hona chahiye hum sabke paas.",
        "Teri high expectations tujhe innovator banati hain. Build what you wish existed!",
        "Bhai, jo cheez tujhe wrong lagti hai — ussi ko fix karne ka tu capable hai. Do it.",
        "Teri taste aur standards? Next level. Never ever lower them for anyone.",
        "Tu excellence demand karta hai — and that's leadership quality number one.",
        "Bhai, teri disgust reaction teri integrity ki proof hai. Rare commodity these days.",
        "Tu settle nahi karta — aur yeh tujhe ordinary se extraordinary banata hai.",
        "Teri yeh quality dekh ke mujhe pata hai — tu kuch sahi banana chahta hai duniya mein.",
        "Bhai, judge karna bura nahi — tera discernment toh teri biggest superpower hai.",
        "Yeh high standards hi tera brand hai. Never compromise on it. Not even once.",
        "Teri nafrut mediocrity se tujhe pushes toward greatness. Always trust that instinct.",
        "Bhai, jo bhi wrong lag raha hai — teri gut bilkul sahi hai. Always trust it.",
    ],
    "neutral": [
        "Bhai, teri yeh calm energy bohot powerful hai. Eye of the storm vibes — respect!",
        "Tera composed rehna duniya mein sabse rare skill hai. Samajh le isko seriously.",
        "Yeh stillness toh teri strength hai — chaos mein bhi tu ground rehta hai. Unreal.",
        "Bhai, teri neutrality dekh ke lagta hai tu sab process kar raha hai andar se. Deep thinker.",
        "Tu stoic hai — aur stoics hi duniya ko change karte hain. History check kar.",
        "Yeh calm face teri biggest asset hai bhai. Don't ever underestimate it.",
        "Teri composed energy dekh ke logon ko anchor milta hai. Tu toh safe harbour hai.",
        "Bhai, teri shanti mein teri strength hai. Sab log yeh nahi kar paate in life.",
        "Yeh still waters toh deep running hain — teri depth tujhe ahead rakhti hai always.",
        "Tu react nahi karta, respond karta hai. That's elite emotional intelligence bhai.",
        "Bhai, teri calm energy se tera team sab se zyada perform karta hoga. Natural leader.",
        "Neutrality toh ek art hai — aur tu master hai iska. Appreciate that.",
        "Tera composed rehna prove karta hai — tu situations se hamesha bada hai.",
        "Bhai, teri yeh grounded energy toh leadership ka core hai. CEO material.",
        "Stability teri superpower hai. Duniya mein chaos hai — tu toh foundation hai.",
        "Tu effortlessly cool hai bhai. That's not taught — that's built over time.",
        "Teri clarity aur calmness dekh ke mujhe bhi shanti aayi. Thank you seriously.",
        "Bhai, tu unshakeable hai. Aur unshakeable log hi lasting things build karte hain.",
        "Yeh neutral face toh ek warrior ki tayyari ka sign hai. Ready mode activated.",
        "Teri stillness mein sab se zyada potential hide hai bhai. Aag lag jaayegi jab nikli!",
    ],
    "unknown": [
        "Bhai, tu toh AI ke liye bhi mystery hai — truly genuinely one of a kind!",
        "Tera face classify nahi hua — kyunki tu classification se bada hai. Legend material.",
        "Undefined? Nahi bhai — tu LIMITLESS hai. That's why no label fits you.",
        "Tu itna unique hai ki mera model confused ho gaya — that's a massive compliment!",
    ],
}

# ════════════════════════════════════════════════════════════════════
#  CSS — PREMIUM DARK UI
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #07070f !important;
    color: #f2f0ec !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 15% 0%, #1d0b3b 0%, #07070f 50%, #0b0a1a 100%) !important;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container { padding: 1.5rem 2.5rem 2rem !important; max-width: 1380px !important; }

.hdr { text-align: center; padding: 1.2rem 0 .8rem; }
.hdr-title {
    font-size: clamp(2rem, 5vw, 3.8rem);
    font-weight: 800; letter-spacing: -.03em;
    background: linear-gradient(135deg, #ff6b35 0%, #ff006e 35%, #8338ec 65%, #3a86ff 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    line-height: 1.1;
}
.hdr-sub {
    font-family: 'JetBrains Mono', monospace; font-size: .72rem;
    color: #3a3a55; letter-spacing: .14em; text-transform: uppercase; margin-top: .4rem;
}

.cam-wrap {
    border-radius: 18px; overflow: hidden; border: 1.5px solid #1e1830;
    background: #0c0b16; box-shadow: 0 0 80px rgba(131,56,236,.12);
}
.cam-wrap img { width: 100%; display: block; border-radius: 16px; }

.emo-card {
    background: rgba(255,255,255,.035); border: 1px solid rgba(255,255,255,.07);
    border-radius: 18px; padding: 1.1rem 1.5rem; text-align: center;
}
.emo-icon { font-size: 3.5rem; line-height: 1; margin-bottom: .25rem; }
.emo-lbl { font-family: 'JetBrains Mono', monospace; font-size: .63rem; color: #555;
    text-transform: uppercase; letter-spacing: .12em; }
.emo-val { font-size: 1.3rem; font-weight: 700; color: #f2f0ec; margin-top: .1rem; }
.conf-lbl { font-family: 'JetBrains Mono', monospace; font-size: .6rem; color: #3a3a55;
    text-align: left; margin: .7rem 0 .25rem; text-transform: uppercase; letter-spacing: .08em; }
.conf-track { background: rgba(255,255,255,.06); border-radius: 8px; height: 6px; overflow: hidden; }
.conf-fill { height: 100%; border-radius: 8px;
    background: linear-gradient(90deg, #8338ec, #ff006e);
    transition: width .7s cubic-bezier(.4,0,.2,1); }

.resp-card {
    border-radius: 20px; padding: 1.4rem 1.7rem; margin-top: .7rem;
    display: flex; align-items: flex-start; gap: 1rem; min-height: 105px;
}
.resp-card.roast {
    background: linear-gradient(135deg, rgba(255,107,53,.12), rgba(255,0,110,.07));
    border: 1px solid rgba(255,80,80,.2);
}
.resp-card.boost {
    background: linear-gradient(135deg, rgba(131,56,236,.12), rgba(58,134,255,.07));
    border: 1px solid rgba(131,56,236,.2);
}
.resp-icon { font-size: 2rem; flex-shrink: 0; margin-top: .15rem; }
.resp-txt { font-size: clamp(.9rem, 1.8vw, 1.1rem); font-weight: 600; line-height: 1.65; color: #f2f0ec; }

.ldots { display: flex; justify-content: center; align-items: center; gap: 8px; padding: 1.8rem; width: 100%; }
.ldot { width: 12px; height: 12px; border-radius: 50%; animation: boing .9s infinite ease-in-out; }
.ldot:nth-child(1) { background: #ff6b35; }
.ldot:nth-child(2) { background: #ff006e; animation-delay: .15s; }
.ldot:nth-child(3) { background: #8338ec; animation-delay: .3s; }
@keyframes boing { 0%, 80%, 100% { transform: scale(.65); opacity: .25; } 40% { transform: scale(1.35); opacity: 1; } }

.status-row { display: flex; align-items: center; gap: .5rem; margin-bottom: .6rem; }
.sdot { width: 7px; height: 7px; border-radius: 50%; background: #22c55e;
    box-shadow: 0 0 7px #22c55e; animation: spulse 2s infinite; }
@keyframes spulse { 0%, 100% { opacity: 1; } 50% { opacity: .2; } }
.stxt { font-family: 'JetBrains Mono', monospace; font-size: .63rem; color: #444;
    text-transform: uppercase; letter-spacing: .1em; }

.badge { display: inline-block; padding: .3rem 1.1rem; border-radius: 100px;
    font-size: .85rem; font-weight: 700; letter-spacing: .03em; }
.roast-b { background: linear-gradient(135deg, #ff4444, #ff8c00); color: #fff; }
.boost-b { background: linear-gradient(135deg, #8338ec, #3a86ff); color: #fff; }
.badge-center { text-align: center; margin: .5rem 0; }

.divider { height: 1px;
    background: linear-gradient(90deg, transparent, rgba(131,56,236,.35), transparent);
    margin: .9rem 0; }

.hist-item { background: rgba(255,255,255,.025); border: 1px solid rgba(255,255,255,.05);
    border-radius: 12px; padding: .7rem 1rem; margin-bottom: .5rem;
    font-size: .82rem; line-height: 1.55; color: #777; }
.hist-meta { font-family: 'JetBrains Mono', monospace; font-size: .62rem; color: #303045;
    margin-bottom: .2rem; text-transform: uppercase; letter-spacing: .08em; }
.hist-empty { font-family: 'JetBrains Mono', monospace; font-size: .7rem; color: #252535; }

.score-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: .5rem; margin-top: .6rem; }
.score-card { background: rgba(255,255,255,.03); border: 1px solid rgba(255,255,255,.06);
    border-radius: 12px; padding: .65rem .8rem; text-align: center; }
.score-num { font-size: 1.8rem; font-weight: 800;
    background: linear-gradient(135deg, #8338ec, #ff006e);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
.score-lbl { font-family: 'JetBrains Mono', monospace; font-size: .58rem; color: #3a3a55;
    text-transform: uppercase; letter-spacing: .08em; margin-top: .1rem; }

.warning-box { background: rgba(255,200,0,.06); border: 1px solid rgba(255,200,0,.2);
    border-radius: 12px; padding: .8rem 1rem; margin-bottom: .8rem;
    font-family: 'JetBrains Mono', monospace; font-size: .72rem; color: #aa9000;
    letter-spacing: .04em; }

footer-bar { text-align: center; margin-top: 2rem; padding: .8rem 0;
    border-top: 1px solid rgba(255,255,255,.04); }
.footer-txt { font-family: 'JetBrains Mono', monospace; font-size: .62rem; color: #1e1e2e;
    letter-spacing: .12em; text-transform: uppercase; text-align: center; }

/* Override Streamlit button styles */
.stButton > button {
    width: 100%; border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important; padding: .7rem 1rem !important;
    transition: all .2s ease !important; letter-spacing: .02em !important;
}
.stButton > button:hover { transform: translateY(-2px) !important; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ════════════════════════════════════════════════════════════════════
STATE_DEFAULTS = {
    "roast_mode": True,
    "last_emotion": "unknown",
    "last_response": "",
    "history": [],
    "confidence": 0.0,
    "total_captures": 0,
    "roast_count": 0,
    "boost_count": 0,
}
for k, v in STATE_DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ════════════════════════════════════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════════

def detect_emotion(frame_bgr):
    """
    Real DeepFace emotion detection.
    Falls back to neutral if DeepFace not installed or no face found.
    """
    if not DEEPFACE_AVAILABLE:
        return "neutral", 55.0

    try:
        result = DeepFace.analyze(
            frame_bgr,
            actions=["emotion"],
            enforce_detection=False,
            detector_backend="opencv",
            silent=True,
        )
        if isinstance(result, list):
            result = result[0]
        dominant = result.get("dominant_emotion", "neutral").lower()
        scores = result.get("emotion", {})
        label_map = {
            "happy": "happy", "sad": "sad", "angry": "angry",
            "surprise": "surprise", "fear": "fear",
            "disgust": "disgust", "neutral": "neutral",
        }
        emotion = label_map.get(dominant, "neutral")
        conf = float(scores.get(dominant, 50.0))
        return emotion, round(conf, 1)
    except Exception:
        return "neutral", 50.0


def draw_face_box(frame_bgr, emotion: str, confidence: float):
    """Draw coloured corner-bracket face box."""
    COLOR_MAP = {
        "happy":    (50,  220, 100),
        "sad":      (100, 130, 255),
        "angry":    (30,  50,  255),
        "surprise": (0,   210, 255),
        "fear":     (0,   160, 255),
        "disgust":  (180, 80,  255),
        "neutral":  (160, 160, 160),
        "unknown":  (100, 100, 100),
    }
    color = COLOR_MAP.get(emotion, (160, 160, 160))
    try:
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        fc = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        faces = fc.detectMultiScale(gray, 1.1, 5, minSize=(80, 80))
        for (x, y, w, h) in faces:
            cs = 22
            corners = [
                [(x + cs, y), (x, y), (x, y + cs)],
                [(x + w - cs, y), (x + w, y), (x + w, y + cs)],
                [(x, y + h - cs), (x, y + h), (x + cs, y + h)],
                [(x + w - cs, y + h), (x + w, y + h), (x + w, y + h - cs)],
            ]
            for pts in corners:
                for i in range(len(pts) - 1):
                    cv2.line(frame_bgr, pts[i], pts[i + 1], color, 2)
            label = f"{EMOTION_EMOJI.get(emotion, '?')} {emotion.upper()}  {confidence:.0f}%"
            cv2.putText(frame_bgr, label, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    except Exception:
        pass
    return frame_bgr


def frame_to_b64(frame_bgr: np.ndarray) -> str:
    """Convert BGR frame to base64 JPEG string."""
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    buf = io.BytesIO()
    Image.fromarray(rgb).save(buf, format="JPEG", quality=82)
    return base64.b64encode(buf.getvalue()).decode()


def get_response(emotion: str, roast_mode: bool) -> str:
    bank = ROASTS if roast_mode else BOOSTS
    lines = bank.get(emotion, bank.get("neutral", ["Kuch samajh nahi aaya bhai!"]))
    return random.choice(lines)


def speak(text: str):
    """Generate audio and autoplay in browser based on chosen engine."""
    engine = st.session_state.get("voice_engine", "Microsoft Edge Neural (Free & Realistic)")
    
    # Remove emojis and sanitize text
    clean = re.sub(r"[^\x00-\x7F\u0900-\u097F\s.,!?\-]", "", text).strip()
    if not clean:
        return
        
    audio_b64 = None
    
    try:
        if "Microsoft Edge Neural" in engine:
            if not EDGE_TTS_AVAILABLE:
                st.warning("⚠️ edge-tts package not available.")
                return
                
            voice = st.session_state.get("edge_voice", "hi-IN-MadhurNeural")
            rate = st.session_state.get("edge_rate", "+10%")
            pitch = st.session_state.get("edge_pitch", "+0Hz")
            
            async def _generate():
                communicate = edge_tts.Communicate(clean, voice, rate=rate, pitch=pitch)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    await communicate.save(f.name)
                    return f.name
                    
            tmp = asyncio.run(_generate())
            with open(tmp, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode()
            os.unlink(tmp)
            
        elif "ElevenLabs" in engine:
            api_key = st.session_state.get("el_api_key", "")
            voice_id = st.session_state.get("el_voice_id", "21m00Tcm4TlvDq8ikWAM")
            model = st.session_state.get("el_model", "eleven_multilingual_v2")
            
            if not api_key:
                st.warning("⚠️ ElevenLabs API Key is missing! Please enter it in the Voice Settings.")
                return
                
            import requests
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": clean,
                "model_id": model,
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.8,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            res = requests.post(url, json=data, headers=headers)
            if res.status_code == 200:
                audio_b64 = base64.b64encode(res.content).decode()
            else:
                st.error(f"❌ ElevenLabs Error: {res.status_code} - {res.text}")
                
        elif "OpenAI" in engine:
            api_key = st.session_state.get("openai_api_key", "")
            voice = st.session_state.get("openai_voice", "fable")
            
            if not api_key:
                st.warning("⚠️ OpenAI API Key is missing! Please enter it in the Voice Settings.")
                return
                
            import requests
            url = "https://api.openai.com/v1/audio/speech"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "tts-1",
                "input": clean,
                "voice": voice
            }
            res = requests.post(url, json=data, headers=headers)
            if res.status_code == 200:
                audio_b64 = base64.b64encode(res.content).decode()
            else:
                st.error(f"❌ OpenAI Error: {res.status_code} - {res.text}")
                
        else:  # Google TTS (Legacy)
            if not GTTS_AVAILABLE:
                st.warning("⚠️ gTTS package is not installed.")
                return
            tts = gTTS(text=clean, lang="hi", slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.save(f.name)
                tmp = f.name
            with open(tmp, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode()
            os.unlink(tmp)
            
        if audio_b64:
            st.markdown(
                f'<audio autoplay style="display:none">'
                f'<source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">'
                f"</audio>",
                unsafe_allow_html=True,
            )
    except Exception as e:
        st.error(f"⚠️ Voice generation failed: {str(e)}")


import threading

# Initialize thread-safe audio queue in session state
if "audio_queue" not in st.session_state:
    st.session_state.audio_queue = []

def bg_speak_worker(text, engine, edge_voice, edge_rate, edge_pitch, el_api_key, el_voice_id, el_model, openai_api_key, openai_voice, queue_list):
    """Background worker to synthesize voice and place it in a thread-safe queue."""
    clean = re.sub(r"[^\x00-\x7F\u0900-\u097F\s.,!?\-]", "", text).strip()
    if not clean:
        return
        
    try:
        audio_b64 = None
        if "Microsoft Edge Neural" in engine:
            if not EDGE_TTS_AVAILABLE:
                return
            async def _generate():
                communicate = edge_tts.Communicate(clean, edge_voice, rate=edge_rate, pitch=edge_pitch)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                    await communicate.save(f.name)
                    return f.name
            tmp = asyncio.run(_generate())
            with open(tmp, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode()
            os.unlink(tmp)
            
        elif "ElevenLabs" in engine:
            if not el_api_key:
                return
            import requests
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{el_voice_id}"
            headers = {
                "xi-api-key": el_api_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": clean,
                "model_id": el_model,
                "voice_settings": {
                    "stability": 0.4,
                    "similarity_boost": 0.8,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            res = requests.post(url, json=data, headers=headers)
            if res.status_code == 200:
                audio_b64 = base64.b64encode(res.content).decode()
                
        elif "OpenAI" in engine:
            if not openai_api_key:
                return
            import requests
            url = "https://api.openai.com/v1/audio/speech"
            headers = {
                "Authorization": f"Bearer {openai_api_key}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "tts-1",
                "input": clean,
                "voice": openai_voice
            }
            res = requests.post(url, json=data, headers=headers)
            if res.status_code == 200:
                audio_b64 = base64.b64encode(res.content).decode()
                
        else:  # Google TTS (Legacy)
            if not GTTS_AVAILABLE:
                return
            tts = gTTS(text=clean, lang="hi", slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
                tts.save(f.name)
                tmp = f.name
            with open(tmp, "rb") as f:
                audio_b64 = base64.b64encode(f.read()).decode()
            os.unlink(tmp)
            
        if audio_b64:
            queue_list.append(audio_b64)
    except Exception:
        pass

def speak_background(text: str):
    """Start a background thread to generate audio and queue it for playback, keeping the UI responsive."""
    if "audio_queue" not in st.session_state:
        st.session_state.audio_queue = []
        
    engine = st.session_state.get("voice_engine", "Microsoft Edge Neural (Free & Realistic)")
    edge_voice = st.session_state.get("edge_voice", "hi-IN-MadhurNeural")
    edge_rate = st.session_state.get("edge_rate", "+10%")
    edge_pitch = st.session_state.get("edge_pitch", "+0Hz")
    el_api_key = st.session_state.get("el_api_key", "")
    el_voice_id = st.session_state.get("el_voice_id", "21m00Tcm4TlvDq8ikWAM")
    el_model = st.session_state.get("el_model", "eleven_multilingual_v2")
    openai_api_key = st.session_state.get("openai_api_key", "")
    openai_voice = st.session_state.get("openai_voice", "fable")
    
    t = threading.Thread(
        target=bg_speak_worker,
        args=(text, engine, edge_voice, edge_rate, edge_pitch, el_api_key, el_voice_id, el_model, openai_api_key, openai_voice, st.session_state.audio_queue),
        daemon=True
    )
    t.start()


# ════════════════════════════════════════════════════════════════════
#  LAYOUT
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div class="hdr">'
    '<div class="hdr-title">🪞 AI Mirror</div>'
    '<div class="hdr-sub">Hinglish Roast Edition · Real Emotion AI · gTTS Voice</div>'
    "</div>",
    unsafe_allow_html=True,
)

# Dependency warnings
if not DEEPFACE_AVAILABLE:
    st.markdown(
        '<div class="warning-box">⚠️  DeepFace not found. '
        "Run: <code>pip install deepface tf-keras</code></div>",
        unsafe_allow_html=True,
    )
if not GTTS_AVAILABLE:
    st.markdown(
        '<div class="warning-box">⚠️  gTTS not found. '
        "Run: <code>pip install gtts</code> for voice output.</div>",
        unsafe_allow_html=True,
    )

col_cam, col_right = st.columns([1.1, 0.9], gap="large")

# ──────────────── LEFT — CAMERA ────────────────────────────────────
with col_cam:
    st.markdown(
        '<div class="status-row"><div class="sdot"></div>'
        '<div class="stxt">Webcam Ready</div></div>',
        unsafe_allow_html=True,
    )

    cam_ph = st.empty()
    cam_ph.markdown(
        '<div class="cam-wrap" style="min-height:300px;display:flex;align-items:center;'
        "justify-content:center;color:#2a2a3a;font-family:'JetBrains Mono',monospace;"
        'font-size:.8rem;">📷 Camera initialising…</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button(
            "🔥 Roast Mode",
            use_container_width=True,
            type="primary" if st.session_state.roast_mode else "secondary",
        ):
            st.session_state.roast_mode = True
            st.rerun()
    with c2:
        if st.button(
            "💖 Boost Mode",
            use_container_width=True,
            type="primary" if not st.session_state.roast_mode else "secondary",
        ):
            st.session_state.roast_mode = False
            st.rerun()

    badge_txt = "🔥 ROAST MODE" if st.session_state.roast_mode else "💖 BOOST MODE"
    badge_cls = "roast-b" if st.session_state.roast_mode else "boost-b"
    st.markdown(
        f'<div class="badge-center"><span class="badge {badge_cls}">{badge_txt}</span></div>',
        unsafe_allow_html=True,
    )

    capture_btn = st.button(
        "📸 Capture & Analyse", use_container_width=True, type="primary"
    )

    voice_on = st.toggle(
        "🔊 Voice Narration",
        value=True,
        key="voice_on_toggle"
    )

    if voice_on:
        with st.expander("🎙️ Voice & Comedian Settings", expanded=False):
            # Select Voice Engine
            engine_options = []
            if EDGE_TTS_AVAILABLE:
                engine_options.append("Microsoft Edge Neural (Free & Realistic)")
            if GTTS_AVAILABLE:
                engine_options.append("Google TTS (Legacy & Robotic)")
            engine_options.extend(["ElevenLabs (Premium Comedian)", "OpenAI (Premium Expressive)"])
            
            voice_engine = st.selectbox(
                "Voice Engine",
                options=engine_options,
                index=0,
                key="voice_engine_select"
            )
            st.session_state.voice_engine = voice_engine
            
            if voice_engine == "Microsoft Edge Neural (Free & Realistic)":
                edge_voice = st.selectbox(
                    "Select Voice",
                    options=[
                        "hi-IN-MadhurNeural (Male - Recommended Hinglish)",
                        "hi-IN-SwaraNeural (Female - Hinglish)",
                        "en-IN-PrabhatNeural (Male - Indian Accent)",
                        "en-IN-NeerjaNeural (Female - Indian Accent)",
                        "en-US-BrianNeural (Male - Expressive)",
                        "en-US-JennyNeural (Female - Expressive)"
                    ],
                    index=0,
                    key="edge_voice_select"
                )
                # Map selectbox string to actual edge-tts voice name
                voice_mapping = {
                    "hi-IN-MadhurNeural (Male - Recommended Hinglish)": "hi-IN-MadhurNeural",
                    "hi-IN-SwaraNeural (Female - Hinglish)": "hi-IN-SwaraNeural",
                    "en-IN-PrabhatNeural (Male - Indian Accent)": "en-IN-PrabhatNeural",
                    "en-IN-NeerjaNeural (Female - Indian Accent)": "en-IN-NeerjaNeural",
                    "en-US-BrianNeural (Male - Expressive)": "en-US-BrianNeural",
                    "en-US-JennyNeural (Female - Expressive)": "en-US-JennyNeural"
                }
                st.session_state.edge_voice = voice_mapping[edge_voice]
                
                st.markdown("<div style='font-size:0.85rem;font-weight:bold;margin-top:0.5rem;'>Stand-up Comedian Tuning</div>", unsafe_allow_html=True)
                
                col_rate, col_pitch = st.columns(2)
                with col_rate:
                    rate_val = st.slider("Speech Speed (Rate)", min_value=-50, max_value=50, value=10, step=5, format="%+d%%", key="edge_rate_slider")
                    # Convert to edge-tts format
                    st.session_state.edge_rate = f"{rate_val:+d}%"
                with col_pitch:
                    pitch_val = st.slider("Voice Pitch Shift", min_value=-20, max_value=20, value=0, step=2, format="%+d Hz", key="edge_pitch_slider")
                    # Convert to edge-tts format
                    st.session_state.edge_pitch = f"{pitch_val:+d}Hz"
                    
            elif voice_engine == "Google TTS (Legacy & Robotic)":
                st.info("Using basic computer-generated voice.")
                
            elif voice_engine == "ElevenLabs (Premium Comedian)":
                st.session_state.el_api_key = st.text_input(
                    "ElevenLabs API Key", 
                    type="password", 
                    value=st.session_state.get("el_api_key", ""),
                    help="Enter your ElevenLabs API Key",
                    key="el_api_key_input"
                )
                st.session_state.el_voice_id = st.text_input(
                    "ElevenLabs Voice ID", 
                    value=st.session_state.get("el_voice_id", "21m00Tcm4TlvDq8ikWAM"),
                    help="Enter a custom Voice ID (cloned or built-in, e.g. Rachel, Drew, Adam)",
                    key="el_voice_id_input"
                )
                st.session_state.el_model = st.selectbox(
                    "Model",
                    options=["eleven_multilingual_v2", "eleven_monolingual_v1"],
                    index=0,
                    key="el_model_select"
                )
                st.markdown(
                    "<div style='font-size:0.75rem;color:#7a7a9a;'>Tip: Go to elevenlabs.io to find or create custom comedian voices!</div>",
                    unsafe_allow_html=True
                )
                
            elif voice_engine == "OpenAI (Premium Expressive)":
                st.session_state.openai_api_key = st.text_input(
                    "OpenAI API Key", 
                    type="password", 
                    value=st.session_state.get("openai_api_key", ""),
                    help="Enter your OpenAI API Key",
                    key="openai_api_key_input"
                )
                openai_voice = st.selectbox(
                    "Select Voice",
                    options=[
                        "fable (Recommended - Expressive & Sarcastic)",
                        "alloy (Neutral & Conversational)",
                        "echo (Balanced & Clear)",
                        "onyx (Deep & Confident Male)",
                        "nova (Bright & High-Energy Female)",
                        "shimmer (Professional & Natural Female)"
                    ],
                    index=0,
                    key="openai_voice_select"
                )
                # Map to OpenAI voice parameter
                voice_mapping_oa = {
                    "fable (Recommended - Expressive & Sarcastic)": "fable",
                    "alloy (Neutral & Conversational)": "alloy",
                    "echo (Balanced & Clear)": "echo",
                    "onyx (Deep & Confident Male)": "onyx",
                    "nova (Bright & High-Energy Female)": "nova",
                    "shimmer (Professional & Natural Female)": "shimmer"
                }
                st.session_state.openai_voice = voice_mapping_oa[openai_voice]

    # Score cards
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""<div class="score-grid">
  <div class="score-card">
    <div class="score-num">{st.session_state.total_captures}</div>
    <div class="score-lbl">Captures</div>
  </div>
  <div class="score-card">
    <div class="score-num">{st.session_state.roast_count}</div>
    <div class="score-lbl">Roasted</div>
  </div>
  <div class="score-card">
    <div class="score-num">{st.session_state.boost_count}</div>
    <div class="score-lbl">Boosted</div>
  </div>
</div>""",
        unsafe_allow_html=True,
    )

# ──────────────── RIGHT — RESULTS ──────────────────────────────────
with col_right:
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:.63rem;'
        "color:#3a3a55;text-transform:uppercase;letter-spacing:.12em;margin-bottom:.5rem;\">"
        "Detected Emotion</div>",
        unsafe_allow_html=True,
    )

    emo_ph  = st.empty()
    resp_ph = st.empty()
    aud_ph  = st.empty()

    def render_emotion(emotion: str, conf: float):
        emoji = EMOTION_EMOJI.get(emotion, "🤔")
        bar_w = min(int(conf), 100)
        emo_ph.markdown(
            f"""<div class="emo-card">
  <div class="emo-icon">{emoji}</div>
  <div class="emo-lbl">AI Detection</div>
  <div class="emo-val">{emotion.upper()}</div>
  <div class="conf-lbl">Confidence — {conf:.0f}%</div>
  <div class="conf-track"><div class="conf-fill" style="width:{bar_w}%"></div></div>
</div>""",
            unsafe_allow_html=True,
        )

    def render_response(text: str, roast: bool):
        icon = "🔥" if roast else "💖"
        cls  = "roast" if roast else "boost"
        resp_ph.markdown(
            f"""<div class="resp-card {cls}">
  <div class="resp-icon">{icon}</div>
  <div class="resp-txt">{text}</div>
</div>""",
            unsafe_allow_html=True,
        )

    render_emotion(st.session_state.last_emotion, st.session_state.confidence)
    if st.session_state.last_response:
        render_response(st.session_state.last_response, st.session_state.roast_mode)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # History
    st.markdown(
        '<div style="font-family:\'JetBrains Mono\',monospace;font-size:.63rem;'
        "color:#3a3a55;text-transform:uppercase;letter-spacing:.12em;margin-bottom:.5rem;\">"
        "Recent Reactions</div>",
        unsafe_allow_html=True,
    )
    hist_ph = st.empty()

    def render_history():
        if not st.session_state.history:
            hist_ph.markdown(
                '<div class="hist-empty">No captures yet — face the mirror!</div>',
                unsafe_allow_html=True,
            )
            return
        html = ""
        for item in reversed(st.session_state.history[-5:]):
            icon = "🔥" if item["mode"] == "roast" else "💖"
            emoji = EMOTION_EMOJI.get(item["emotion"], "")
            html += (
                f'<div class="hist-item"><div class="hist-meta">'
                f"{icon} {item['mode'].upper()} · {item['emotion'].upper()} {emoji}"
                f"</div>{item['text']}</div>"
            )
        hist_ph.markdown(html, unsafe_allow_html=True)

    render_history()

# ════════════════════════════════════════════════════════════════════
#  CAPTURE LOGIC
# ════════════════════════════════════════════════════════════════════
if capture_btn:
    cap = cv2.VideoCapture(0)
    # Warm up camera
    for _ in range(5):
        cap.read()
    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        st.error(
            "❌ Webcam not accessible! "
            "Check that it's connected and permissions are granted."
        )
    else:
        # Show raw frame instantly
        cam_ph.markdown(
            f'<div class="cam-wrap">'
            f'<img src="data:image/jpeg;base64,{frame_to_b64(frame)}"/>'
            f"</div>",
            unsafe_allow_html=True,
        )

        # Loading animation
        cls_name = "roast" if st.session_state.roast_mode else "boost"
        resp_ph.markdown(
            f'<div class="resp-card {cls_name}" style="justify-content:center">'
            '<div class="ldots"><div class="ldot"></div>'
            '<div class="ldot"></div><div class="ldot"></div></div></div>',
            unsafe_allow_html=True,
        )

        time.sleep(0.7)  # Dramatic tension

        # ── REAL DEEPFACE DETECTION ──
        emotion, confidence = detect_emotion(frame)
        st.session_state.last_emotion  = emotion
        st.session_state.confidence    = confidence

        # Draw annotated frame
        annotated = draw_face_box(frame.copy(), emotion, confidence)
        cam_ph.markdown(
            f'<div class="cam-wrap">'
            f'<img src="data:image/jpeg;base64,{frame_to_b64(annotated)}"/>'
            f"</div>",
            unsafe_allow_html=True,
        )

        # Generate & display response
        response = get_response(emotion, st.session_state.roast_mode)
        st.session_state.last_response = response

        with col_right:
            render_emotion(emotion, confidence)
            render_response(response, st.session_state.roast_mode)
            if voice_on:
                with aud_ph:
                    speak(response)

        # Update stats
        st.session_state.total_captures += 1
        if st.session_state.roast_mode:
            st.session_state.roast_count += 1
        else:
            st.session_state.boost_count += 1

        st.session_state.history.append({
            "mode":    "roast" if st.session_state.roast_mode else "boost",
            "emotion": emotion,
            "text":    response,
        })
        render_history()

# ════════════════════════════════════════════════════════════════════
#  CONTINUOUS LIVE ROAST MODE
# ════════════════════════════════════════════════════════════════════
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col_live_left, col_live_right = st.columns([1, 1])
with col_live_left:
    live_roast_on = st.toggle(
        "🤖 Continuous Live Roast Mode",
        value=False,
        key="live_roast_toggle",
        help="The AI will continuously watch you through the webcam and roast or boost you every few seconds!"
    )
with col_live_right:
    roast_interval = st.slider(
        "Roast Interval (seconds)",
        min_value=3,
        max_value=10,
        value=4,
        step=1,
        key="live_roast_interval",
        disabled=not live_roast_on
    )

if live_roast_on:
    # Clear any stale audio from a previous session
    st.session_state.audio_queue = []
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error("❌ Webcam not accessible! Please check connection and permissions.")
    else:
        # Warm up camera
        for _ in range(5):
            cap.read()
            
        last_roast_time = 0
        last_emotion = "unknown"
        last_confidence = 0.0
        
        status_box = st.empty()
        status_box.info("🎥 Live camera active! AI is watching your emotions...")
        
        try:
            while st.session_state.get("live_roast_toggle", False):
                # Check for queued background audio and play it immediately
                if "audio_queue" in st.session_state and st.session_state.audio_queue:
                    audio_b64 = st.session_state.audio_queue.pop(0)
                    with aud_ph:
                        st.markdown(
                            f'<audio autoplay style="display:none">'
                            f'<source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">'
                            f"</audio>",
                            unsafe_allow_html=True,
                        )

                ret, frame = cap.read()
                if not ret or frame is None:
                    status_box.error("❌ Lost webcam connection!")
                    break
                    
                current_time = time.time()
                
                # Trigger a new roast at the specified interval
                if current_time - last_roast_time >= roast_interval:
                    # Capture the current frame for DeepFace analysis
                    emotion, confidence = detect_emotion(frame)
                    last_emotion = emotion
                    last_confidence = confidence
                    st.session_state.last_emotion = emotion
                    st.session_state.confidence = confidence
                    
                    # Generate roast/boost response
                    response = get_response(emotion, st.session_state.roast_mode)
                    st.session_state.last_response = response
                    
                    # Play voice narration in background
                    if voice_on:
                        speak_background(response)
                        
                    # Update stats
                    st.session_state.total_captures += 1
                    if st.session_state.roast_mode:
                        st.session_state.roast_count += 1
                    else:
                        st.session_state.boost_count += 1
                        
                    st.session_state.history.append({
                        "mode": "roast" if st.session_state.roast_mode else "boost",
                        "emotion": emotion,
                        "text": response,
                    })
                    
                    # Update right column results in real-time
                    with col_right:
                        render_emotion(emotion, confidence)
                        render_response(response, st.session_state.roast_mode)
                        render_history()
                        
                    last_roast_time = current_time
                
                # Draw the face bounding box in real-time (using fast Haar Cascades and the last detected emotion color)
                annotated_frame = draw_face_box(frame.copy(), last_emotion, last_confidence)
                
                # Update the main camera viewfinder
                cam_ph.markdown(
                    f'<div class="cam-wrap">'
                    f'<img src="data:image/jpeg;base64,{frame_to_b64(annotated_frame)}"/>'
                    f"</div>",
                    unsafe_allow_html=True,
                )
                
                # Sleep a tiny bit to maintain smooth FPS and prevent CPU hogging
                time.sleep(0.05)
                
        except Exception as e:
            status_box.error(f"⚠️ Live Mode Error: {str(e)}")
        finally:
            cap.release()
            status_box.empty()
            # Restore the default camera placeholder when turned off
            cam_ph.markdown(
                '<div class="cam-wrap" style="min-height:300px;display:flex;align-items:center;'
                "justify-content:center;color:#2a2a3a;font-family:'JetBrains Mono',monospace;"
                'font-size:.8rem;">📷 Camera initialising…</div>',
                unsafe_allow_html=True,
            )

# ════════════════════════════════════════════════════════════════════
#  VIRAL FEATURES SECTION
# ════════════════════════════════════════════════════════════════════
with st.expander("🚀 Viral Features Roadmap"):
    st.markdown("""
**🎮 Multiplayer Roast Battle**  
Two webcams, one screen. AI analyses both faces simultaneously and judges who gets the more savage roast. Crowd votes via QR code link.

**🏆 Emotion Leaderboard**  
Track which emotion you trigger most across sessions. Share your personalised "Roast Score" badge on social media.

**📸 Shareable Roast Card**  
Auto-generates a meme card: your face + detected emotion + roast text + logo. One-click WhatsApp/Instagram share.

**🎙️ 30-Second Roast Reel**  
Record a 30-sec video, AI analyses emotion frame-by-frame and produces a highlight reel with voice narration.

**📊 Emotion Timeline Chart**  
Live line chart showing your emotional journey across 10+ captures — fun for presentations!

**🤖 Live Roast Mode**  
Continuous detection every 3 seconds with live TTS — like a roast machine gun.
""")

# ════════════════════════════════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════════════════════════════════
st.markdown(
    '<div style="text-align:center;margin-top:2rem;padding:.8rem 0;'
    "border-top:1px solid rgba(255,255,255,.04);\">"
    '<p class="footer-txt">AI Mirror v2 · Hinglish Roast Edition · '
    "DeepFace + gTTS + Streamlit · No GPU Required</p></div>",
    unsafe_allow_html=True,
)
