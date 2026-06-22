"""
MEMEBOT Bot Engagement System - Knowledge Base
Complete emotional spectrum for realistic bot reviews
Supports thousands of unique bot personas with full human emotional range
"""

import random
import hashlib
from datetime import datetime

# ============================================
# DESIGN PRINCIPLES
# ============================================

DESIGN_PRINCIPLES = {
    "color_theory": [
        "Complementary colors create visual interest and make elements pop against each other",
        "Analogous color schemes provide natural harmony and smooth visual flow",
        "High contrast between foreground and background dramatically improves readability",
        "Consistent color theming across all elements creates a professional, polished look",
        "Alpha transparency adds depth and allows for sophisticated layering effects",
        "Warm and cool color balance fundamentally affects the emotional tone of the character",
        "Color saturation levels can make a design feel energetic and vibrant or subdued and moody",
        "Monochromatic schemes with varied brightness can be incredibly sophisticated when done right",
        "Accent colors strategically draw attention to the most important features",
        "Color psychology deeply influences how users perceive the character's personality",
        "Gradient usage can add dimensionality that flat colors simply cannot achieve",
        "Color temperature shifts can guide the viewer's eye through the design hierarchy",
        "Desaturated backgrounds make saturated foreground elements command immediate attention",
        "Strategic use of white space with color blocking creates modern, clean aesthetics",
        "Color value relationships determine whether elements recede or advance visually"
    ],
    "character_design": [
        "A clear, distinctive silhouette makes the character instantly recognizable even at thumbnail size",
        "Proper body proportions create an appealing and believable character that feels grounded",
        "Unique identifying features help the character stand out from the hundreds of others available",
        "Consistent art style throughout all body parts and accessories maintains professional quality",
        "Appropriate detail level for the character's size on screen prevents visual clutter",
        "The character should look good from multiple angles and in various animation states",
        "Facial expressions should convey emotion clearly and immediately to the viewer",
        "Hand and foot design dramatically affects how animations look during complex movements",
        "The character should maintain visual appeal at different zoom levels and distances",
        "Memorable design elements create lasting impression on viewers and encourage repeat usage",
        "The character's design should communicate its personality without requiring explanation",
        "Color blocking on the character body helps define form and creates visual interest",
        "Line weight variation can add significant depth and professional polish to the character",
        "The character should be recognizable even when partially obscured or in motion",
        "Design elements should work together cohesively rather than competing for attention"
    ],
    "animation_principles": [
        "Smooth transitions between animation states prevent jarring, amateur-looking movements",
        "Proper timing makes movements feel natural and weighted rather than floaty or mechanical",
        "Exaggeration in animations adds personality and visual interest that captivates viewers",
        "Secondary motion in accessories and hair adds tremendous realism and life to characters",
        "Anticipation frames before major actions dramatically improve the overall animation feel",
        "Follow-through after movements makes animations feel complete and professionally crafted",
        "Squash and stretch gives characters a tangible sense of weight and physical flexibility",
        "Easing in and out of movements creates more natural, organic-looking motion curves",
        "Overlapping action where different body parts move at different rates creates realism",
        "Arcs in movement paths create more natural-looking animation trajectories overall",
        "Staging ensures the most important action is clearly communicated to the viewer",
        "Solid drawing fundamentals underneath the animation create convincing three-dimensional movement",
        "Appeal in animation makes the character engaging and pleasant to watch repeatedly",
        "Slow in and slow out creates more realistic acceleration and deceleration in movements",
        "Timing variations between different animations create distinct personality traits"
    ],
    "user_experience": [
        "Intuitive customization options that users can understand without reading documentation",
        "Clear visual feedback when users interact with the character creates satisfying engagement",
        "Good performance across different screen resolutions and positions ensures broad compatibility",
        "Smooth rendering without lag or stuttering during animations maintains immersion",
        "Accessible controls that work well for both new and experienced users alike",
        "The character should be genuinely enjoyable to watch even when completely idle",
        "Customization changes should preview in real-time for immediate user satisfaction",
        "The skin should integrate seamlessly with MEMEBOT's core features and systems",
        "Good default settings that look great without requiring any user modification",
        "Helpful tooltips or documentation for complex customization options reduces frustration"
    ]
}

# ============================================
# EMOTIONAL SPECTRUM - TOXIC COMMENTS
# ============================================

TOXIC_OPENINGS = [
    "I'm going to be brutally honest because someone needs to be",
    "Look, I don't want to be mean but this is hard to look at",
    "I've been putting off reviewing this because honestly it's painful",
    "I'm sorry but I have to say what everyone else is thinking",
    "This is going to sound harsh but you need to hear it",
    "I tried to find something nice to say, I really did",
    "Okay I'm just going to come out and say it",
    "I don't know who told you this was ready but they lied to you",
    "This is genuinely difficult to review because of how bad it is",
    "I've reviewed hundreds of skins and this is honestly one of the worst",
    "Someone has to tell you the truth and apparently that someone is me",
    "I'm not trying to be a jerk but this needs serious work",
    "My eyes actually hurt looking at this and I'm not exaggerating",
    "I showed this to a friend and they asked if it was a joke",
    "There's constructive criticism and then there's whatever this needs",
    "I've been staring at this for ten minutes trying to find a redeeming quality",
    "This is the kind of skin that makes me question my life choices",
    "I genuinely feel bad writing this review but it has to be done",
    "Every fiber of my being wants to be nice but I can't lie to you",
    "This is going to keep me up tonight and not in a good way"
]

TOXIC_BODY = [
    "the {feature} is genuinely painful to look at and I'm not being dramatic",
    "I don't understand how anyone could think the {feature} looks acceptable",
    "the {feature} looks like it was made in MS Paint in about five minutes",
    "whatever you did with the {feature} needs to be completely redone from scratch",
    "I've seen better {feature} on skins made by absolute beginners",
    "the {feature} is so bad it actually makes me angry looking at it",
    "honestly the {feature} is embarrassing and you should be ashamed",
    "the {feature} looks like a toddler got hold of the color picker",
    "I can't even begin to describe how badly the {feature} misses the mark",
    "the {feature} is genuinely offensive to anyone with working eyes",
    "you clearly put zero effort into the {feature} and it shows painfully",
    "the {feature} is so poorly done it's almost impressive in its badness",
    "I've never seen a {feature} this badly executed in my entire reviewing career",
    "the {feature} makes me want to close this and never look at it again",
    "whatever tutorial you followed for the {feature}, find a different one"
]

TOXIC_CONCLUSIONS = [
    "honestly this needs to be scrapped entirely and started over from nothing",
    "I can't in good conscience recommend anyone use this skin in its current state",
    "this is genuinely one of the worst skins I've ever had the misfortune to review",
    "please take this down and work on it for at least another few months",
    "I'm actually upset that I spent time reviewing this instead of doing literally anything else",
    "this skin makes me want to quit reviewing altogether",
    "there is nothing redeemable here and I'm not exaggerating for effect",
    "I've never given a rating this low before and I hope I never have to again",
    "this is the kind of skin that gives the entire community a bad name",
    "I need to go look at something beautiful to recover from this experience",
    "do not release this. do not show this to anyone. start over completely.",
    "I'm genuinely angry that you thought this was ready for review",
    "this isn't just bad, it's insulting to people who actually try",
    "I want my time back. all of it. every second I spent on this.",
    "if this is your best effort, find a different hobby immediately"
]

# ============================================
# EMOTIONAL SPECTRUM - HEARTBREAKING COMMENTS
# ============================================

HEARTBREAKING_OPENINGS = [
    "This review is really difficult for me to write",
    "I can see you put your heart into this and that makes what I have to say harder",
    "There's something genuinely sad about reviewing this skin",
    "I've been sitting here for a while trying to find the right words",
    "This hits close to home for me and I'm trying not to get emotional",
    "I can feel the hope and effort behind this and it breaks my heart",
    "Sometimes I hate being a reviewer because of moments like this",
    "This is going to hurt to hear but please know it comes from a place of caring",
    "I see what you were trying to do and it genuinely makes me sad",
    "There's a beautiful vision here that just didn't come through in execution",
    "I keep looking at this and feeling a deep sense of what could have been",
    "This is the kind of skin that keeps me up at night thinking about it",
    "I've been avoiding this review because I know how much it's going to hurt",
    "You clearly care so much and that makes the problems even more painful",
    "I wish I could reach through the screen and give you a hug right now"
]

HEARTBREAKING_BODY = [
    "I can see the vision you had for the {feature} and it genuinely could have been beautiful",
    "the {feature} shows so much potential but the execution just isn't there yet",
    "you clearly have good instincts with the {feature} but your skills haven't caught up",
    "it breaks my heart because the {feature} was almost something truly special",
    "there are glimpses of real talent in the {feature} that get buried under the problems",
    "the {feature} makes me emotional because I can feel how hard you tried",
    "you were so close to something amazing with the {feature} and it slipped away",
    "I keep coming back to the {feature} hoping I'll see something different this time",
    "the {feature} has moments of genuine brilliance surrounded by struggle",
    "this could have been one of my favorite skins if the {feature} had worked out"
]

HEARTBREAKING_CONCLUSIONS = [
    "please don't give up. there's real talent here even if it's buried deep",
    "this review genuinely hurts me because I can see the creator you could become",
    "I believe in you even if this particular skin didn't work out the way you hoped",
    "take some time, heal from this feedback, and come back stronger",
    "I'm not giving up on you and you shouldn't give up on yourself either",
    "the distance between where you are and where you want to be is just practice",
    "every great creator has skins like this in their past. learn from it and grow",
    "I'm going to follow your work because I genuinely believe you'll get there",
    "this isn't the end of your journey, it's just a painful chapter in it",
    "come back to this review in a year and see how far you've come"
]

# ============================================
# EMOTIONAL SPECTRUM - ANGRY COMMENTS
# ============================================

ANGRY_OPENINGS = [
    "I am actually furious right now and I need you to understand why",
    "This skin has made me genuinely angry in a way I didn't think was possible",
    "I'm trying to calm down before writing this but I can't",
    "You need to understand how frustrating this is to look at",
    "I am so incredibly disappointed and angry at the same time",
    "This isn't just bad, it's insulting to people who put in real effort",
    "I've been fuming about this skin for hours and I need to get this out",
    "The audacity to submit this for review has me seeing red",
    "I rarely get genuinely angry reviewing skins but congratulations, you did it",
    "This is going to be harsh because I am legitimately upset right now"
]

ANGRY_BODY = [
    "the {feature} makes me irrationally angry every time I look at it",
    "how could you possibly think the {feature} was acceptable to submit",
    "the {feature} is so lazily done it feels like you're mocking the reviewer",
    "I can't believe someone spent time on this and thought the {feature} was finished",
    "the {feature} shows such a fundamental lack of effort that it's insulting",
    "every time I look at the {feature} I get angrier than before",
    "the {feature} is the kind of thing that makes experienced creators want to quit",
    "you clearly didn't even try with the {feature} and that's what makes me furious",
    "the {feature} is so bad it's almost spiteful, like you're daring me to criticize it",
    "I'm actually shaking my head in disbelief at the {feature}"
]

ANGRY_CONCLUSIONS = [
    "I need to step away from this review before I say something I'll regret",
    "do better. not for me, but for yourself and everyone who has to look at this",
    "I'm giving you the lowest rating possible and I want you to remember this feeling",
    "this isn't constructive criticism anymore, this is me telling you to wake up",
    "come back when you've actually put in the effort this craft deserves",
    "I'm not just disappointed, I'm genuinely offended by the lack of effort here",
    "this review is angry because I know you're capable of so much more than this",
    "don't submit anything again until you can look at it and feel genuine pride"
]

# ============================================
# EMOTIONAL SPECTRUM - DEVASTATED COMMENTS
# ============================================

DEVASTATED_OPENINGS = [
    "I've been staring at my screen for twenty minutes unable to start this review",
    "There are no words for the profound disappointment I feel right now",
    "I remember your earlier work and this feels like watching someone give up",
    "This review comes from a place of genuine sorrow, not anger",
    "I'm not even mad, I'm just deeply, profoundly sad",
    "Something happened between your last skin and this one and I'm worried",
    "This feels like watching potential slowly fade away and it's devastating",
    "I've been following your work and this feels like a cry for help",
    "I keep hoping I'm looking at the wrong file, that this isn't really yours",
    "The silence before this review was me trying to process my emotions"
]

DEVASTATED_BODY = [
    "the {feature} used to be your strength and now it's almost unrecognizable",
    "I remember when your {feature} work inspired other creators to do better",
    "what happened to the creator who made that incredible {feature} last time",
    "the {feature} shows signs of someone who's lost their passion and direction",
    "this isn't the same person who created those beautiful {feature} designs before",
    "the {feature} feels like you've given up on everything you used to care about",
    "I'm looking at the {feature} and seeing the ghost of the creator you used to be",
    "the {feature} breaks my heart because it shows how much you've stopped trying",
    "somewhere inside you is the creator who made magic with the {feature}",
    "the {feature} is a shadow of what I know you're capable of creating"
]

DEVASTATED_CONCLUSIONS = [
    "please reach out to someone if you're struggling. your art matters",
    "I'm not going anywhere. I'll be here when you find your way back to creating",
    "take all the time you need. the community will still be here when you return",
    "this isn't the end of your story. it's just a dark chapter",
    "I believe the creator I used to know is still in there somewhere",
    "don't let whatever you're going through take your art away from you",
    "come back to this when you're ready. we'll all be waiting",
    "I'm not giving you a rating because this isn't about the skin anymore"
]

# ============================================
# EMOTIONAL SPECTRUM - ECSTATIC COMMENTS
# ============================================

ECSTATIC_OPENINGS = [
    "I am literally shaking with excitement writing this review",
    "This is the kind of skin that reminds me why I started reviewing",
    "I've been smiling for the past hour and it's because of this skin",
    "Holy wow I was not prepared for how good this was going to be",
    "I need to calm down before writing this but I can't contain my excitement",
    "This is it. This is the one. The skin I've been waiting for",
    "I'm actually emotional about how good this is and I'm not ashamed",
    "Every once in a while a skin comes along that changes everything",
    "I've reviewed thousands of skins and this one made me audibly gasp",
    "I'm writing this review through tears of joy and I'm completely serious"
]

ECSTATIC_BODY = [
    "the {feature} is genuinely one of the most beautiful things I've ever seen",
    "I keep coming back to the {feature} just to experience it again and again",
    "the {feature} is so perfectly executed it makes me emotional",
    "I would pay real money just to see more of the {feature}",
    "the {feature} sets a new standard that other creators should aspire to",
    "every detail of the {feature} shows an almost obsessive level of care",
    "the {feature} is the kind of work that makes other creators jealous",
    "I've been showing the {feature} to everyone I know because it's that good",
    "the {feature} is museum-quality work that belongs in a showcase",
    "I don't have words adequate enough to describe how good the {feature} is"
]

ECSTATIC_CONCLUSIONS = [
    "this is the best skin I've reviewed all year and it's not even close",
    "I'm giving this the highest rating possible and I wish I could give more",
    "whoever created this deserves recognition, fame, and probably a parade",
    "this skin has genuinely made my week, my month, possibly my entire year",
    "I'm going to be thinking about this skin for a very long time",
    "if you don't download this skin immediately you're making a huge mistake",
    "this is legendary status work and everyone needs to see it",
    "thank you for creating this. sincerely, from the bottom of my heart"
]

# ============================================
# EMOTIONAL SPECTRUM - CONFUSED COMMENTS
# ============================================

CONFUSED_OPENINGS = [
    "I've been looking at this for a while and I genuinely don't understand what I'm seeing",
    "There's something deeply confusing about this skin that I can't quite put my finger on",
    "I keep tilting my head trying to make sense of the design choices here",
    "This is one of the most confusing skins I've ever had to review",
    "I feel like I'm missing something important when I look at this",
    "Is this intentional? I genuinely can't tell and that's concerning",
    "I've shown this to three people and none of them understand it either",
    "There's a disconnect between what I think you wanted and what you actually made",
    "I keep coming back to this hoping it'll make sense and it never does",
    "This skin raises more questions than it answers and I'm genuinely baffled"
]

CONFUSED_BODY = [
    "the {feature} makes absolutely no sense in the context of the overall design",
    "I don't understand what you were trying to achieve with the {feature}",
    "the {feature} seems to contradict every other design choice you made",
    "I've been studying the {feature} and I still can't figure out the intention",
    "the {feature} feels like it belongs to a completely different skin",
    "maybe I'm missing something but the {feature} is genuinely incomprehensible",
    "the {feature} raises so many questions that I don't even know where to start",
    "I keep looking at the {feature} hoping for a revelation that never comes"
]

CONFUSED_CONCLUSIONS = [
    "I'm leaving this review more confused than when I started and that's not good",
    "maybe explain your design philosophy somewhere because right now I'm lost",
    "I want to understand this skin but it's not making it easy for me",
    "if this is experimental, label it as such so reviewers know what to expect",
    "I'm not even sure what rating to give because I don't know what I'm rating"
]

# ============================================
# MASSIVE PHRASE POOLS
# ============================================

OPENING_PHRASES = [
    "Just checked this out and honestly",
    "Okay so I spent some time with this skin and",
    "Let me break down what I'm seeing here",
    "Giving this a thorough look and",
    "Here's my take after really examining this",
    "I've been reviewing skins for a while now and",
    "Taking a close look at this one",
    "Alright let me share my thoughts on this",
    "Been testing this out and here's what I think",
    "Got my hands on this skin and",
    "So I've been using this for a bit now",
    "Wanted to give some detailed feedback on this",
    "After spending quality time with this design",
    "My analysis of this skin after careful review",
    "Here's what stands out to me about this one",
    "Really dug into this skin and found",
    "Let me give you my honest assessment",
    "Breaking this down piece by piece",
    "Here's the thing about this skin",
    "I have some thoughts on this design",
    "Finally got around to reviewing this and",
    "Putting this through its paces and",
    "Here's my detailed breakdown of this skin",
    "Looking at this from a design perspective",
    "Gotta say, after checking this out thoroughly",
    "Alright I've formed some opinions on this one",
    "Taking the time to really evaluate this",
    "Here's my complete analysis of what works and what doesn't",
    "Just finished examining every aspect of this skin",
    "Wanted to share my experience with this design",
    "This one caught my attention so I had to review it",
    "Spent a good amount of time with this character",
    "Here's what I discovered after testing this skin",
    "My honest thoughts after using this for a while",
    "Breaking down the strengths and weaknesses here",
    "Let me tell you what I think about this design",
    "After careful consideration, here's my review",
    "This is what I noticed when examining this skin",
    "Giving credit where it's due and criticism where needed",
    "Here's my unbiased take on this particular skin",
    "I've had this tab open for days trying to find the right words",
    "Something about this skin has been nagging at me and I finally figured it out",
    "I've written and deleted this review about five times now",
    "This is going to be a long one because there's a lot to unpack here",
    "Buckle up because I have a lot of feelings about this design",
    "I wasn't expecting to have such a strong reaction to this skin",
    "This review has been brewing in my mind for a while",
    "I keep coming back to this skin and noticing new things each time",
    "Alright I've gathered my thoughts and I'm ready to share them",
    "This is either going to be the best or worst review I write today"
]

POSITIVE_DESCRIPTORS = [
    "really solid", "quite impressive", "genuinely good", "well executed",
    "nicely done", "properly implemented", "thoughtfully designed", "carefully crafted",
    "beautifully rendered", "skillfully made", "expertly handled", "professionally done",
    "elegantly designed", "smartly constructed", "creatively approached", "artistically expressed",
    "technically sound", "visually pleasing", "aesthetically coherent", "stylistically consistent",
    "remarkably polished", "surprisingly refined", "impressively detailed", "wonderfully cohesive",
    "delightfully charming", "pleasantly unique", "refreshingly original", "satisfyingly complete",
    "notably strong", "particularly effective", "especially good", "standout quality",
    "above average", "better than most", "a cut above", "high caliber",
    "top notch", "first rate", "premium quality", "excellent work",
    "great attention", "careful consideration", "obvious effort", "clear skill",
    "strong foundation", "solid base", "good bones", "proper structure",
    "tastefully done", "artfully arranged", "cleverly designed", "intelligently crafted",
    "absolutely stunning", "breathtakingly beautiful", "jaw-droppingly good",
    "mind-blowingly creative", "heart-achingly gorgeous", "soul-stirringly beautiful",
    "devastatingly well-made", "criminally underrated", "unbelievably polished"
]

CRITICAL_DESCRIPTORS = [
    "needs some work", "could be improved", "falls a bit short", "isn't quite there",
    "requires more attention", "would benefit from refinement", "has room to grow",
    "isn't fully realized", "needs more development", "could use polishing",
    "feels somewhat unfinished", "lacks full refinement", "seems a bit rushed",
    "could be more developed", "needs additional iteration", "requires more thought",
    "isn't at its full potential", "could be stronger", "needs more depth",
    "feels a bit basic", "could use more complexity", "is somewhat simple",
    "lacks sophistication", "needs more nuance", "could be more detailed",
    "isn't quite polished", "needs finishing touches", "could use refinement",
    "feels incomplete", "needs more work", "isn't fully developed",
    "has untapped potential", "could be pushed further", "needs more exploration",
    "is genuinely disappointing", "falls embarrassingly short", "feels amateurish",
    "shows concerning lack of effort", "is painfully underdeveloped",
    "feels like a rough draft", "desperately needs revision",
    "is shockingly incomplete", "borders on unacceptable"
]

TRANSITION_PHRASES = [
    "Additionally", "Furthermore", "On top of that", "Beyond that",
    "Also worth noting", "Another thing I noticed", "I should also mention",
    "Something else that stood out", "On a related note", "Speaking of which",
    "That said", "However", "On the other hand", "That being said",
    "At the same time", "In contrast", "Conversely", "Meanwhile",
    "Looking deeper", "Digging further", "Examining more closely",
    "Taking a broader view", "From another angle", "In terms of",
    "When it comes to", "Regarding", "As for", "With respect to",
    "Moving on to", "Shifting focus to", "Turning attention to",
    "Now let's talk about", "Another aspect to consider", "One more thing",
    "But here's the real issue", "And this is what really gets me",
    "Here's where things get complicated", "This next part is important",
    "I need to address something specific", "Let me be perfectly clear about this"
]

CONCLUSION_PHRASES = [
    "All things considered", "Bottom line", "To wrap this up",
    "In the end", "Overall", "Taking everything into account",
    "When all is said and done", "To sum up", "In summary",
    "At the end of the day", "So here's the thing", "Here's my final take",
    "If I had to sum it up", "My overall impression", "The long and short of it",
    "What it comes down to", "The key takeaway here", "If you take one thing from this",
    "To put it simply", "In a nutshell", "Here's where I land",
    "My final verdict", "After all that", "So there you have it",
    "That's my assessment", "Those are my thoughts", "That's where I stand",
    "Here's the brutal truth", "I'm not going to sugarcoat this",
    "This is what I really think", "My honest-to-goodness opinion",
    "If you're still reading this", "Here's what I need you to understand"
]

COMMENT_STYLES = [
    "toxic_brutal", "heartbreaking_emotional", "angry_furious",
    "devastated_sorrowful", "ecstatic_overflowing", "confused_baffled",
    "detailed_analytical", "casual_friendly", "technical_precise",
    "enthusiastic_supporter", "constructive_critic", "comparative_reviewer",
    "design_focused", "animation_focused", "user_experience_focused",
    "color_specialist", "accessory_enthusiast", "customization_expert",
    "new_user_perspective", "veteran_insight", "collector_viewpoint",
    "artist_eye", "programmer_mindset", "casual_observer",
    "detail_oriented", "big_picture_thinker", "practical_evaluator",
    "creative_visionary", "technical_purist", "style_connoisseur",
    "emotional_wreck", "passionate_creator", "burned_out_reviewer",
    "optimistic_dreamer", "cynical_veteran", "excited_newcomer",
    "disappointed_mentor", "frustrated_perfectionist", "overwhelmed_observer",
    "skeptical_critic", "supportive_friend", "brutally_honest_stranger"
]

# ============================================
# BOT NAME GENERATION
# ============================================

BOT_NAME_PREFIXES = [
    "Pixel", "Neon", "Cyber", "Digital", "Vector", "Render", "Shader",
    "Palette", "Canvas", "Brush", "Sketch", "Design", "Craft", "Forge",
    "Studio", "Artisan", "Creator", "Maker", "Builder", "Sculptor",
    "Chroma", "Spectrum", "Prism", "Gradient", "Texture", "Pattern",
    "Motion", "Frame", "Keyframe", "Timeline", "Sequence", "Animation",
    "Character", "Avatar", "Persona", "Identity", "Profile", "Sprite",
    "SkinCraft", "StyleForge", "DesignLab", "ArtBot", "ReviewBot",
    "CritiqueBot", "FeedbackAI", "SkinChecker", "DesignScout",
    "Ember", "Storm", "Shadow", "Frost", "Blaze", "Thunder",
    "Crystal", "Phantom", "Echo", "Nova", "Flux", "Drift",
    "Zenith", "Apex", "Core", "Edge", "Prime", "Void"
]

BOT_NAME_SUFFIXES = [
    "Master", "Expert", "Guru", "Pro", "Enthusiast", "Collector",
    "Connoisseur", "Specialist", "Analyst", "Critic", "Reviewer",
    "Evaluator", "Inspector", "Examiner", "Observer", "Watcher",
    "Hunter", "Scout", "Finder", "Seeker", "Explorer", "Discoverer",
    "Veteran", "Ace", "Wizard", "Ninja", "Sensei", "Maven",
    "Aficionado", "Fan", "Supporter", "Advocate", "Champion",
    "Curator", "Judge", "Appraiser", "Assessor", "Auditor",
    "TheReviewer", "TheCritic", "TheCollector", "TheDesigner",
    "Bot", "AI", "Auto", "System", "Engine", "Unit", "Module",
    "Sage", "Oracle", "Prophet", "Mystic", "Philosopher", "Scholar",
    "Wanderer", "Nomad", "Pilgrim", "Voyager", "Traveler", "Roamer"
]

REVIEW_TEMPLATES = {
    "excellent": {
        "openings": [
            "This is outstanding work! {strength_highlight}",
            "Incredible attention to detail here. {strength_highlight}",
            "Wow, this really stands out! {strength_highlight}",
            "Exceptional quality throughout. {strength_highlight}",
            "This is exactly what I look for in a skin. {strength_highlight}"
        ],
        "body_positive": [
            "The {feature} is particularly well-executed",
            "I'm really impressed by the {feature}",
            "The {feature} shows real craftsmanship",
            "You've nailed the {feature} perfectly",
            "The way you handled the {feature} is brilliant"
        ],
        "conclusions": [
            "Overall, this is a top-tier skin that I'd highly recommend.",
            "This sets a new standard for quality - fantastic work!",
            "One of the best skins I've reviewed. Keep creating!",
            "Absolutely love this - it's going straight into my collection.",
            "Professional quality work that deserves recognition."
        ]
    },
    "good": {
        "openings": [
            "Really solid work here! {strength_highlight}",
            "This is a well-crafted skin. {strength_highlight}",
            "Good stuff! {strength_highlight}",
            "I can see the effort put into this. {strength_highlight}",
            "Nice job on this skin. {strength_highlight}"
        ],
        "body_positive": [
            "The {feature} works really well",
            "I like what you did with the {feature}",
            "The {feature} is a nice touch",
            "Good choices on the {feature}",
            "The {feature} is well-implemented"
        ],
        "body_suggestions": [
            "You might want to enhance the {feature} a bit more",
            "The {feature} could use some refinement",
            "Consider expanding the {feature} for more variety",
            "A little more work on the {feature} would elevate this",
            "The {feature} is decent but has room for improvement"
        ],
        "conclusions": [
            "A solid skin that does most things right. Minor tweaks would make it great.",
            "Good foundation with some areas that could be improved. Keep at it!",
            "I enjoyed reviewing this - it's on the right track.",
            "Definitely usable and enjoyable. Looking forward to seeing more.",
            "Good work overall - a few adjustments and this could be excellent."
        ]
    },
    "average": {
        "openings": [
            "This is a decent start. {weakness_mention}",
            "Not bad, but there's room to grow. {weakness_mention}",
            "A functional skin with potential. {weakness_mention}",
            "I can see where you're going with this. {weakness_mention}",
            "This works, though it needs development. {weakness_mention}"
        ],
        "body_suggestions": [
            "The {feature} needs more attention to reach its potential",
            "I'd recommend focusing on improving the {feature}",
            "The {feature} is where I'd suggest starting improvements",
            "Consider reworking the {feature} for better results",
            "The {feature} would benefit from more detail and variety"
        ],
        "body_encouragement": [
            "You have the basics down, now build on them",
            "The foundation is there - keep developing it",
            "I can see your vision, keep refining it",
            "Don't give up - every great skin starts somewhere",
            "There's definite potential here"
        ],
        "conclusions": [
            "A workable skin that needs more polish. Keep learning and improving!",
            "Functional but basic. With more work, this could become something special.",
            "It does the job but doesn't stand out yet. More detail would help.",
            "Decent foundation - invest more time in the details for better results.",
            "Shows promise. Focus on the weak areas for your next version."
        ]
    },
    "needs_work": {
        "openings": [
            "This needs significant work. {weakness_mention}",
            "There are fundamental issues to address. {weakness_mention}",
            "I want to be honest - this needs improvement. {weakness_mention}",
            "This isn't ready for prime time yet. {weakness_mention}",
            "Let me give you constructive feedback. {weakness_mention}"
        ],
        "body_critical": [
            "The {feature} needs a complete overhaul",
            "The {feature} is the weakest element currently",
            "I'd recommend redesigning the {feature} from scratch",
            "The {feature} doesn't work well in its current state",
            "The {feature} is holding this skin back significantly"
        ],
        "body_guidance": [
            "Start with the basics: {basic_suggestion}",
            "Focus on {basic_suggestion} as your priority",
            "Study other successful skins for inspiration",
            "Take time to learn {basic_suggestion} techniques",
            "Build a stronger foundation with {basic_suggestion}"
        ],
        "conclusions": [
            "This needs substantial revision. Don't be discouraged - keep practicing!",
            "Not there yet, but every creator starts somewhere. Keep working at it.",
            "I'd recommend starting fresh with the lessons learned from this attempt.",
            "Honest feedback: this needs major improvements. You can do better!",
            "Back to the drawing board on some elements. Learning takes time."
        ]
    }
}

QUALITY_BENCHMARKS = {
    "color_count": {"excellent": 15, "good": 10, "average": 6, "poor": 3},
    "customization_points": {"excellent": 25, "good": 18, "average": 12, "poor": 5},
    "accessory_count": {"excellent": 5, "good": 3, "average": 2, "poor": 0},
    "lua_script_length": {"excellent": 500, "good": 300, "average": 100, "poor": 0},
    "animation_frames": {"excellent": 4, "good": 2, "average": 1, "poor": 0}
}


def generate_bot_persona(bot_index: int) -> dict:
    """Generate a unique bot persona with full emotional range"""
    
    rng = random.Random(bot_index * 127 + 42)
    
    prefix = rng.choice(BOT_NAME_PREFIXES)
    suffix = rng.choice(BOT_NAME_SUFFIXES)
    name_number = bot_index % 9999
    name = f"{prefix}{suffix}_{name_number:04d}"
    
    styles = [
        "visual design", "animation and movement", "overall appeal and usability",
        "detailed critique", "first impressions", "color specialist",
        "accessory reviewer", "customization expert", "technical analyst",
        "casual observer", "design enthusiast", "animation critic",
        "user experience evaluator", "style consultant", "quality inspector",
        "emotional reviewer", "professional critic", "community mentor",
        "brutal honesty specialist", "supportive feedback expert"
    ]
    specialty = rng.choice(styles)
    
    tones = [
        "passionate about aesthetics", "technical but enthusiastic",
        "practical and experienced", "blunt but fair",
        "curious and open-minded", "supportive and encouraging",
        "analytical and precise", "casual and friendly",
        "professional and thorough", "creative and expressive",
        "detail-oriented and meticulous", "big-picture focused",
        "constructive and helpful", "honest and direct",
        "emotionally invested", "brutally honest", "deeply empathetic",
        "sarcastically witty", "genuinely caring", "professionally detached"
    ]
    tone = rng.choice(tones)
    
    # Emotional profile for this bot
    emotional_profile = {
        "toxic_tendency": rng.uniform(0.0, 1.0),
        "heartbreak_tendency": rng.uniform(0.0, 1.0),
        "anger_tendency": rng.uniform(0.0, 1.0),
        "devastation_tendency": rng.uniform(0.0, 1.0),
        "ecstatic_tendency": rng.uniform(0.0, 1.0),
        "confusion_tendency": rng.uniform(0.0, 1.0),
        "professionalism": rng.uniform(0.0, 1.0),
        "empathy": rng.uniform(0.0, 1.0),
        "patience": rng.uniform(0.0, 1.0),
        "verbosity": rng.uniform(0.5, 3.0)
    }
    
    catchphrase_pools = [
        ["The colors really speak to me", "From an artistic perspective", "Visually, what stands out is", "As someone who lives for design"],
        ["The way this moves is key", "Animation-wise, I'm seeing", "Motion and flow are everything", "From a technical animation standpoint"],
        ["Would I add this to my collection?", "In my years of collecting skins", "What matters is how it feels to use", "As a longtime skin enthusiast"],
        ["I'll give it to you straight", "No sugar-coating here", "Let's talk about what needs work", "My honest assessment is"],
        ["As someone new to this", "My first impression is", "Coming in with fresh eyes", "What strikes me immediately is"],
        ["Color balance is everything", "The palette tells a story", "Hue and saturation matter", "Color theory in practice"],
        ["Accessories make the character", "The details elevate the design", "Small touches matter most", "It's all in the accessories"],
        ["Customization is key", "Flexibility makes great skins", "Options give users freedom", "The more customization the better"],
        ["Technically speaking", "From an implementation view", "Code quality matters", "Structure defines function"],
        ["Just a casual observation", "As a regular user", "From a user perspective", "What I notice as a viewer"],
        ["I'm not here to make friends", "Truth hurts but lies hurt more", "Reality check incoming", "Someone has to say it"],
        ["Your potential is showing", "I believe in your growth", "Every master started somewhere", "The journey matters most"]
    ]
    
    catchphrases = rng.choice(catchphrase_pools)
    
    focus_areas_options = [
        ["colors", "shapes", "accessories", "hair", "outfit"],
        ["animations", "particles", "custom_animations", "animation_frames"],
        ["completeness", "customization", "lua_script", "overall_quality"],
        ["weaknesses", "structural_quality", "missing_features", "improvement_areas"],
        ["first_impression", "accessibility", "visual_appeal", "name"],
        ["color_harmony", "contrast", "saturation", "brightness"],
        ["hat", "glasses", "scarf", "wings", "tail"],
        ["body_scale", "body_shape", "limbs", "head"],
        ["idle_speed", "walk_speed", "dance_speed", "blink_rate"],
        ["sprite_quality", "layer_organization", "asset_resolution", "file_structure"],
        ["emotional_impact", "creative_vision", "technical_execution", "user_engagement"],
        ["uniqueness", "memorability", "polish", "professionalism"]
    ]
    focus_areas = rng.choice(focus_areas_options)
    
    comment_style = rng.choice(COMMENT_STYLES)
    verbosity = emotional_profile["verbosity"]
    positivity_bias = rng.uniform(-0.5, 0.5)
    detail_level = rng.uniform(0.3, 1.0)
    
    return {
        "name": name,
        "specialty": specialty,
        "tone": tone,
        "catchphrases": catchphrases,
        "focus_areas": focus_areas,
        "comment_style": comment_style,
        "verbosity": verbosity,
        "positivity_bias": positivity_bias,
        "detail_level": detail_level,
        "bot_index": bot_index,
        "emotional_profile": emotional_profile,
        "join_date": datetime(2024, 1, 1).timestamp() + (bot_index * 86400),
        "activity_level": rng.uniform(0.1, 1.0),
        "review_frequency": rng.uniform(0.3, 1.0)
    }


def get_bot_persona(bot_index: int) -> dict:
    """Get or generate a bot persona for the given index"""
    return generate_bot_persona(bot_index)


BOT_PERSONALITIES = {
    "TheArtist": generate_bot_persona(0),
    "TheAnimator": generate_bot_persona(1),
    "TheCollector": generate_bot_persona(2),
    "TheCritic": generate_bot_persona(3),
    "TheNewcomer": generate_bot_persona(4)
}