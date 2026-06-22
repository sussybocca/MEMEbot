"""
MEMEBOT Bot Engagement System - AI Review Engine
Generates intelligent, contextual reviews based on skin analysis
Uses knowledge base and design principles to create authentic feedback
Supports thousands of bots with unique personalities and slow organic engagement
Full emotional spectrum: toxic, heartbreaking, angry, devastated, ecstatic, confused
Reviews range from 1000-3000 words with genuine human-like emotional depth
"""

import random
import math
import hashlib
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timedelta
from knowledge_base import (
    DESIGN_PRINCIPLES, REVIEW_TEMPLATES, get_bot_persona,
    QUALITY_BENCHMARKS, OPENING_PHRASES, POSITIVE_DESCRIPTORS,
    CRITICAL_DESCRIPTORS, TRANSITION_PHRASES, CONCLUSION_PHRASES,
    TOXIC_OPENINGS, TOXIC_BODY, TOXIC_CONCLUSIONS,
    HEARTBREAKING_OPENINGS, HEARTBREAKING_BODY, HEARTBREAKING_CONCLUSIONS,
    ANGRY_OPENINGS, ANGRY_BODY, ANGRY_CONCLUSIONS,
    DEVASTATED_OPENINGS, DEVASTATED_BODY, DEVASTATED_CONCLUSIONS,
    ECSTATIC_OPENINGS, ECSTATIC_BODY, ECSTATIC_CONCLUSIONS,
    CONFUSED_OPENINGS, CONFUSED_BODY, CONFUSED_CONCLUSIONS
)


class AIReviewer:
    """Generates contextual reviews based on skin analysis data with full emotional range"""
    
    def __init__(self, skin_analyzer=None):
        self.skin_analyzer = skin_analyzer
        self.review_history = []
        self.used_phrases = set()
        self.review_count = 0
        self.total_bots_available = 5000
        self.bots_reviewed = set()
        self.submission_start_time = None
        self.global_phrase_tracker = {}
    
    def set_submission_start_time(self, start_time: datetime):
        """Set when the submission was made for organic growth calculation"""
        self.submission_start_time = start_time
    
    def get_available_bot_count(self, days_elapsed: float) -> int:
        """Calculate how many bots have discovered this skin based on time elapsed"""
        if days_elapsed <= 0:
            return 0
        
        if days_elapsed < 1:
            return random.randint(1, 3)
        elif days_elapsed < 7:
            return int(days_elapsed * random.uniform(2, 5))
        elif days_elapsed < 30:
            return int(days_elapsed * random.uniform(8, 20))
        elif days_elapsed < 90:
            return int(days_elapsed * random.uniform(30, 80))
        elif days_elapsed < 365:
            return int(days_elapsed * random.uniform(100, 500))
        else:
            return min(
                self.total_bots_available,
                int(days_elapsed * random.uniform(1000, 5000))
            )
    
    def get_views_for_day(self, days_elapsed: float, skin_quality: float) -> int:
        """Calculate organic views for a given day based on time and quality"""
        if days_elapsed <= 0:
            return 0
        
        base_views = 0
        
        if days_elapsed < 1:
            base_views = random.randint(0, 2)
        elif days_elapsed < 3:
            base_views = random.randint(1, 5)
        elif days_elapsed < 7:
            base_views = random.randint(3, 15)
        elif days_elapsed < 14:
            base_views = random.randint(10, 40)
        elif days_elapsed < 30:
            base_views = random.randint(20, 100)
        elif days_elapsed < 60:
            base_views = random.randint(50, 300)
        elif days_elapsed < 90:
            base_views = random.randint(100, 800)
        elif days_elapsed < 180:
            base_views = random.randint(200, 2000)
        elif days_elapsed < 365:
            base_views = random.randint(500, 10000)
        else:
            base_views = random.randint(1000, 50000)
        
        quality_mult = 0.5 + (skin_quality / 10.0)
        random_factor = random.uniform(0.5, 1.5)
        
        return max(0, int(base_views * quality_mult * random_factor))
    
    def get_likes_for_views(self, views: int, skin_quality: float, days_elapsed: float) -> int:
        """Calculate realistic likes based on views"""
        base_like_rate = 0.02 + (skin_quality / 10.0) * 0.15
        
        if days_elapsed < 7:
            base_like_rate *= 1.3
        elif days_elapsed < 30:
            base_like_rate *= 1.1
        
        like_rate = base_like_rate * random.uniform(0.7, 1.3)
        
        return max(0, int(views * like_rate))
    
    def _determine_emotional_state(self, overall_score: float, bot_persona: Dict) -> str:
        """Determine which emotional state the bot will write from based on score and persona"""
        emotional_profile = bot_persona.get('emotional_profile', {})
        
        if overall_score >= 8.5:
            # High quality - mostly ecstatic, some analytical
            weights = {
                'ecstatic': emotional_profile.get('ecstatic_tendency', 0.5) * 3.0,
                'analytical': 2.0,
                'confused': 0.1,
                'toxic': 0.01,
                'heartbreaking': 0.05,
                'angry': 0.01,
                'devastated': 0.01
            }
        elif overall_score >= 7.0:
            # Good quality - mixed positive
            weights = {
                'analytical': 3.0,
                'ecstatic': emotional_profile.get('ecstatic_tendency', 0.5) * 1.5,
                'confused': 0.3,
                'toxic': 0.02,
                'heartbreaking': 0.1,
                'angry': 0.05,
                'devastated': 0.05
            }
        elif overall_score >= 5.0:
            # Average - mixed reactions
            weights = {
                'analytical': 2.0,
                'confused': 1.5,
                'heartbreaking': emotional_profile.get('heartbreak_tendency', 0.5) * 1.5,
                'angry': emotional_profile.get('anger_tendency', 0.5) * 1.0,
                'toxic': emotional_profile.get('toxic_tendency', 0.5) * 0.8,
                'devastated': emotional_profile.get('devastation_tendency', 0.5) * 0.8,
                'ecstatic': 0.1
            }
        elif overall_score >= 3.0:
            # Below average - critical emotions
            weights = {
                'toxic': emotional_profile.get('toxic_tendency', 0.5) * 2.0,
                'angry': emotional_profile.get('anger_tendency', 0.5) * 2.0,
                'devastated': emotional_profile.get('devastation_tendency', 0.5) * 1.5,
                'heartbreaking': emotional_profile.get('heartbreak_tendency', 0.5) * 1.5,
                'confused': 1.0,
                'analytical': 0.5,
                'ecstatic': 0.01
            }
        else:
            # Very poor - extreme negative emotions
            weights = {
                'toxic': emotional_profile.get('toxic_tendency', 0.5) * 3.0,
                'angry': emotional_profile.get('anger_tendency', 0.5) * 2.5,
                'devastated': emotional_profile.get('devastation_tendency', 0.5) * 2.0,
                'heartbreaking': emotional_profile.get('heartbreak_tendency', 0.5) * 1.5,
                'confused': 1.0,
                'analytical': 0.3,
                'ecstatic': 0.0
            }
        
        # Normalize weights and pick
        total = sum(weights.values())
        if total == 0:
            return 'analytical'
        
        rand = random.uniform(0, total)
        cumulative = 0
        for state, weight in weights.items():
            cumulative += weight
            if rand <= cumulative:
                return state
        
        return 'analytical'
    
    def generate_review(self, analysis: Dict, bot_persona: Dict, 
                       days_elapsed: float = 0) -> Dict:
        """Generate a complete review with full emotional depth and 1000-3000 words"""
        
        overall_score = analysis.get('overall_score', 5.0)
        scores = analysis.get('scores', {})
        strengths = analysis.get('strengths', [])
        weaknesses = analysis.get('weaknesses', [])
        suggestions = analysis.get('suggestions', [])
        metrics = analysis.get('metrics', {})
        skin_name = analysis.get('skin_name', 'this skin')
        
        emotional_state = self._determine_emotional_state(overall_score, bot_persona)
        quality_tier = self._determine_tier(overall_score)
        rating = self._calculate_rating(overall_score, bot_persona)
        
        # Build the massive review
        review_sections = []
        
        # Opening paragraph (emotional, 100-300 words)
        opening = self._generate_emotional_opening(
            emotional_state, quality_tier, bot_persona, 
            strengths, weaknesses, skin_name, overall_score
        )
        review_sections.append(opening)
        
        # Personal connection paragraph (100-200 words)
        personal = self._generate_personal_connection(
            emotional_state, bot_persona, overall_score, skin_name
        )
        review_sections.append(personal)
        
        # Detailed analysis section (300-800 words)
        analysis_section = self._generate_detailed_analysis(
            emotional_state, quality_tier, bot_persona, scores, 
            metrics, strengths, weaknesses, suggestions
        )
        review_sections.append(analysis_section)
        
        # Emotional reaction section (150-400 words)
        emotional_reaction = self._generate_emotional_reaction(
            emotional_state, bot_persona, overall_score, 
            strengths, weaknesses, skin_name
        )
        review_sections.append(emotional_reaction)
        
        # Specific feature breakdown (200-500 words)
        feature_breakdown = self._generate_feature_breakdown(
            emotional_state, bot_persona, scores, metrics, 
            strengths, weaknesses
        )
        review_sections.append(feature_breakdown)
        
        # Comparison to other work (100-300 words)
        comparison = self._generate_comparison_section(
            emotional_state, bot_persona, overall_score, skin_name
        )
        review_sections.append(comparison)
        
        # Constructive advice section (100-300 words)
        advice = self._generate_advice_section(
            emotional_state, quality_tier, weaknesses, suggestions, bot_persona
        )
        review_sections.append(advice)
        
        # Future outlook section (100-200 words)
        future = self._generate_future_outlook(
            emotional_state, bot_persona, overall_score, skin_name
        )
        review_sections.append(future)
        
        # Conclusion (100-300 words)
        conclusion = self._generate_emotional_conclusion(
            emotional_state, quality_tier, bot_persona, overall_score, skin_name
        )
        review_sections.append(conclusion)
        
        # AI disclaimer
        ai_disclaimer = self._generate_ai_disclaimer(bot_persona, emotional_state)
        review_sections.append(ai_disclaimer)
        
        review_text = '\n\n'.join(review_sections)
        
        review = {
            'bot_name': bot_persona.get('name', 'Anonymous Bot'),
            'bot_persona': bot_persona.get('specialty', 'general'),
            'rating': rating,
            'review_text': review_text,
            'quality_tier': quality_tier,
            'emotional_state': emotional_state,
            'generated_at': datetime.now().isoformat(),
            'word_count': len(review_text.split()),
            'review_id': self.review_count,
            'bot_index': bot_persona.get('bot_index', -1),
            'days_elapsed': days_elapsed
        }
        
        self.review_count += 1
        self.review_history.append(review)
        self.bots_reviewed.add(bot_persona.get('bot_index', -1))
        
        return review
    
    def _determine_tier(self, overall_score: float) -> str:
        if overall_score >= 8.5:
            return "excellent"
        elif overall_score >= 7.0:
            return "good"
        elif overall_score >= 5.0:
            return "average"
        else:
            return "needs_work"
    
    def _calculate_rating(self, overall_score: float, bot_persona: Dict) -> int:
        base_rating = (overall_score / 10.0) * 5.0
        positivity_bias = bot_persona.get('positivity_bias', 0.0)
        random_factor = random.uniform(-0.4, 0.4)
        final_rating = base_rating + positivity_bias + random_factor
        final_rating = max(1.0, min(5.0, final_rating))
        return round(final_rating)
    
    def _generate_emotional_opening(self, emotional_state: str, tier: str, 
                                   persona: Dict, strengths: List, weaknesses: List,
                                   skin_name: str, overall_score: float) -> str:
        """Generate a deeply emotional opening paragraph (100-300 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0))
        bot_name = persona.get('name', 'I')
        
        paragraphs = []
        
        if emotional_state == 'toxic':
            opener = rng.choice(TOXIC_OPENINGS)
            paragraphs.append(opener)
            
            # Add extra toxic detail
            toxic_details = [
                f"I've literally been staring at {skin_name} for the past twenty minutes trying to find something, anything positive to say. I've looked at the colors, the shapes, the animations, the customization options, and every single time I think I've found something redeeming, I look closer and realize I was wrong. This is genuinely exhausting.",
                f"Let me be perfectly clear about something: when I review skins, I want to like them. I want to find the good in every creation. But {skin_name} has defeated me. It has worn me down with its complete disregard for basic design principles and left me wondering why I even bother doing this anymore.",
                f"I've reviewed skins that were made by complete beginners who had never opened a design program before. I've reviewed skins that were clearly rushed and unfinished. But {skin_name} is different. It's not just bad - it's actively frustrating to look at. It's the kind of bad that makes you question the creator's decision-making process at every turn."
            ]
            paragraphs.append(rng.choice(toxic_details))
            
        elif emotional_state == 'heartbreaking':
            opener = rng.choice(HEARTBREAKING_OPENINGS)
            paragraphs.append(opener)
            
            heartbreaking_details = [
                f"I can see you, the creator, sitting there working on {skin_name}. I can see the hours you put in, the late nights, the moments where you thought you'd finally gotten something right. And that's what makes this so hard. You clearly care so much, and the gap between what you wanted to create and what actually came out is just... it's heartbreaking.",
                f"There's something about {skin_name} that keeps me coming back. Not because it's good - it's not. But because I can feel the hope embedded in every pixel. I can feel the creator's dreams, their aspirations, their genuine desire to make something beautiful. And seeing those dreams fall short is genuinely painful.",
                f"I've been putting off writing this review because I know how much it's going to hurt to read. But I also know that avoiding the truth doesn't help anyone. So here I am, trying to find the words to tell you that {skin_name} isn't working, while also trying to tell you that I believe in you anyway."
            ]
            paragraphs.append(rng.choice(heartbreaking_details))
            
        elif emotional_state == 'angry':
            opener = rng.choice(ANGRY_OPENINGS)
            paragraphs.append(opener)
            
            angry_details = [
                f"I am genuinely furious about {skin_name}. Not because it's bad - bad skins are a dime a dozen and I've learned to deal with them. I'm furious because this could have been good. The potential is RIGHT THERE staring me in the face and instead of reaching for it, the creator just... didn't. They settled. They gave up. They submitted something that's maybe 40% of what it could have been and expected everyone to be okay with that.",
                f"You know what really gets me about {skin_name}? The laziness. The sheer, unadulterated laziness of it. I can see exactly where the creator stopped trying. I can point to the specific elements where they decided 'good enough' was acceptable. And that makes me angrier than if they'd just made something completely terrible, because at least then I'd know they didn't know better.",
                f"I've been fuming about {skin_name} for three days now. Three days of this skin living rent-free in my head, making me angry every time I think about it. And you want to know the worst part? I'm not even sure the creator will read this review. I'm not sure they'll care. That's what really gets me - the possibility that all this anger is for nothing."
            ]
            paragraphs.append(rng.choice(angry_details))
            
        elif emotional_state == 'devastated':
            opener = rng.choice(DEVASTATED_OPENINGS)
            paragraphs.append(opener)
            
            devastated_details = [
                f"I remember when I first discovered this creator's work. There was something special there - a spark, a unique perspective, a voice that stood out from the crowd. And now, looking at {skin_name}, I'm searching for that spark and coming up empty. What happened? Where did that creator go? What extinguished that fire that used to burn so brightly?",
                f"There's a particular kind of sadness that comes from watching someone lose their way. {skin_name} isn't just a bad skin - it's evidence of something deeper going wrong. It's like watching a friend slowly give up on their dreams, one compromise at a time, until what's left is just a hollow shell of what they used to create.",
                f"I keep looking at {skin_name} and hoping I'm wrong. Hoping that maybe I'm just not seeing it correctly, that there's some hidden genius I'm missing. But there isn't. What I'm seeing is someone who's lost their creative direction, and it's devastating to witness. I'm not angry. I'm not disappointed. I'm just deeply, profoundly sad."
            ]
            paragraphs.append(rng.choice(devastated_details))
            
        elif emotional_state == 'ecstatic':
            opener = rng.choice(ECSTATIC_OPENINGS)
            paragraphs.append(opener)
            
            ecstatic_details = [
                f"I need you to understand something about {skin_name}. I have reviewed literally thousands of skins. Thousands. And in all that time, only a handful have made me feel the way this one does. It's not just that it's good - there are plenty of good skins out there. It's that it's special. It has that indefinable quality that separates the technically proficient from the genuinely inspired.",
                f"I've been showing {skin_name} to everyone I know. My friends who don't even care about MEMEBOT have had to sit through me gushing about this skin. My family thinks I've lost my mind because I won't stop talking about the color choices and the animation flow. But I don't care. When something is this good, it deserves to be celebrated.",
                f"There are moments in a reviewer's career where everything changes. Where you see something that raises the bar so high that it fundamentally alters your understanding of what's possible. {skin_name} is one of those moments. This isn't just a great skin - it's a paradigm shift. It's the kind of work that other creators will study and try to emulate for years to come."
            ]
            paragraphs.append(rng.choice(ecstatic_details))
            
        elif emotional_state == 'confused':
            opener = rng.choice(CONFUSED_OPENINGS)
            paragraphs.append(opener)
            
            confused_details = [
                f"I've been trying to understand {skin_name} for a while now and I'm still not sure I do. It's not that it's bad exactly - although some parts definitely are. It's that it doesn't make sense. The design choices contradict each other. The color palette seems to be fighting itself. The animations suggest one thing while the static design suggests another entirely.",
                f"Every time I think I've figured out what {skin_name} is trying to be, I notice something else that undermines that interpretation. It's like the skin can't decide what it wants to be when it grows up. Is it edgy? Is it cute? Is it serious? Is it playful? The answer seems to be 'yes to all of the above' and that's exactly the problem.",
                f"I've shown {skin_name} to several other reviewers and asked them what they think it's supposed to be. None of them could give me a clear answer. That's not a good sign. When multiple experienced reviewers can't figure out the core concept of your skin, you've got a fundamental communication problem."
            ]
            paragraphs.append(rng.choice(confused_details))
            
        else:  # analytical
            opener = rng.choice(OPENING_PHRASES)
            paragraphs.append(opener)
            
            analytical_details = [
                f"After spending considerable time with {skin_name}, I've developed a comprehensive understanding of its strengths and weaknesses. This review will break down each aspect systematically, providing clear, actionable feedback that I hope will be useful for future development.",
                f"My approach to reviewing {skin_name} is methodical. I examine color theory, design completeness, animation readiness, customization depth, and structural quality as separate categories before synthesizing them into an overall assessment.",
                f"Let me walk you through my analysis of {skin_name}. I'll start with the visual elements, move through the technical implementation, and finish with the user experience considerations that ultimately determine whether a skin succeeds or fails."
            ]
            paragraphs.append(rng.choice(analytical_details))
        
        return ' '.join(paragraphs)
    
    def _generate_personal_connection(self, emotional_state: str, persona: Dict,
                                     overall_score: float, skin_name: str) -> str:
        """Generate a personal connection paragraph (100-200 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 10)
        bot_name = persona.get('name', 'I')
        specialty = persona.get('specialty', 'design')
        
        if emotional_state == 'toxic':
            templates = [
                f"As someone who specializes in {specialty}, I take personal offense to what I'm seeing in {skin_name}. This isn't just a bad skin - it's an insult to the craft that I've dedicated countless hours to mastering. When I see work like this, it makes me feel like all the time I've spent learning and improving was for nothing, because apparently anyone can just throw something together and call it finished.",
                f"I've been doing this for years. I've developed my eye, refined my taste, learned to appreciate the subtle differences between good design and great design. And then {skin_name} comes along and it's like none of that matters. It's like the creator didn't even try to learn the basics before submitting this. That's not just frustrating - it's personally insulting.",
                f"Every reviewer has their breaking point. The skin that finally makes them snap. For me, {skin_name} might be that skin. I've tried to be patient. I've tried to find the good. But at some point, you have to call it what it is: a complete and utter failure that shows zero respect for the craft or the people who take it seriously."
            ]
        elif emotional_state == 'heartbreaking':
            templates = [
                f"I specialize in {specialty}, and I can tell you from experience that the journey from beginner to proficient is long and difficult. I see so much of my younger self in {skin_name} - the ambition, the excitement, the desire to create something amazing. But I also see the same mistakes I made, the same painful lessons I had to learn. And knowing how much those lessons hurt me, it breaks my heart to know you'll have to go through them too.",
                f"There's a version of {skin_name} that exists in the creator's mind. A beautiful, polished, perfect version. I know because I've had that same vision for my own work. And the gap between that vision and reality is one of the most painful things a creative person can experience. Looking at this skin, I can feel that gap viscerally.",
                f"I've been where you are. I've created work that I was proud of, only to have it torn apart by reviewers who didn't understand my vision. But here's the thing - they were right. And as much as it hurts to hear, I need to be right too. {skin_name} isn't working. But that doesn't mean you're not a creator. It just means you're still learning."
            ]
        elif emotional_state == 'angry':
            templates = [
                f"I've spent years developing my expertise in {specialty}. Years of practice, study, failure, and growth. So when I see {skin_name}, I don't just see a bad skin - I see wasted potential. I see someone who could have been great but chose to be mediocre instead. And that choice, that deliberate decision to not push harder, makes me genuinely angry.",
                f"As a {specialty} specialist, I can tell you exactly what's wrong with {skin_name}. I can point to specific techniques that should have been used, specific principles that were ignored, specific standards that weren't met. But the thing that really gets me isn't the technical failures - it's the attitude. The apparent belief that this level of quality is acceptable.",
                f"I didn't get to where I am in {specialty} by accepting mediocrity from myself. I pushed. I struggled. I failed and got back up and failed again until I finally succeeded. And that's why {skin_name} makes me so angry - because I know the creator didn't push. They didn't struggle. They just gave up and submitted whatever this is."
            ]
        elif emotional_state == 'devastated':
            templates = [
                f"My background in {specialty} has taught me that growth is never linear. Creators have ups and downs, breakthroughs and setbacks. But {skin_name} doesn't feel like a setback - it feels like a surrender. It feels like someone who was on an upward trajectory suddenly decided to stop climbing and slide all the way back down.",
                f"I've been in the {specialty} space long enough to recognize when someone is going through something. The signs are all over {skin_name} - the lack of attention to detail, the shortcuts, the unfinished elements. This isn't the work of someone who's lazy or untalented. This is the work of someone who's struggling, and that breaks my heart.",
                f"As someone who's dedicated their life to {specialty}, I know how much it hurts when your work doesn't live up to your own standards. But I also know that the only way through that pain is to keep creating. And looking at {skin_name}, I'm worried that the creator might not make it through. I'm worried this might be the end of their journey."
            ]
        elif emotional_state == 'ecstatic':
            templates = [
                f"In all my years specializing in {specialty}, I've rarely encountered work that makes me feel the way {skin_name} does. It's the kind of work that reminds me why I fell in love with this craft in the first place. It's the kind of work that makes me want to be a better creator myself.",
                f"My expertise in {specialty} means I'm usually the one teaching others, pointing out flaws, suggesting improvements. But {skin_name} has humbled me. There are techniques here that I've never seen before, approaches that I would never have thought of. This skin isn't just good - it's educational.",
                f"As a {specialty} specialist, I'm supposed to be the expert. But I'll be honest - I've learned things from studying {skin_name} that I'll be applying to my own work. That's the highest compliment I can give. When a skin teaches the teacher something new, you know it's something truly special."
            ]
        elif emotional_state == 'confused':
            templates = [
                f"My training in {specialty} usually helps me quickly assess what a skin is trying to accomplish. But {skin_name} has me stumped. The signals are mixed, the intentions unclear. It's like trying to read a book where every other chapter is from a different genre.",
                f"As someone who's spent years developing my eye for {specialty}, I usually trust my instincts. But {skin_name} has me second-guessing myself. Am I missing something? Is there a deeper meaning I'm not seeing? Or is it genuinely as confused as it appears?",
                f"I've consulted my {specialty} colleagues about {skin_name}, and for the first time in my career, none of us could reach a consensus. Some saw potential, others saw disaster. The fact that we couldn't agree on something as basic as whether the skin is good or bad tells you everything you need to know."
            ]
        else:
            templates = [
                f"My experience in {specialty} allows me to evaluate {skin_name} from an informed perspective. I've seen enough skins to know what works and what doesn't, and I'll be drawing on that knowledge throughout this review.",
                f"As a {specialty} reviewer, I approach {skin_name} with both technical knowledge and an appreciation for creative expression. The best skins balance these two elements, and I'll be examining how well this one achieves that balance.",
                f"My background in {specialty} gives me a particular lens through which to view {skin_name}. I notice details that casual users might miss, and I understand the technical challenges involved in implementing certain features."
            ]
        
        return rng.choice(templates)
    
    def _generate_detailed_analysis(self, emotional_state: str, tier: str,
                                   persona: Dict, scores: Dict, metrics: Dict,
                                   strengths: List, weaknesses: List,
                                   suggestions: List) -> str:
        """Generate detailed analysis section (300-800 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 20)
        
        sections = []
        
        # Color analysis
        color_score = scores.get('color_harmony', 5)
        color_metrics = metrics.get('color', {})
        unique_colors = color_metrics.get('unique_colors', 0)
        
        if color_score >= 7:
            sections.append(f"The color work in this skin is genuinely impressive. With {unique_colors} unique colors in the palette, there's enough variety to create visual interest without becoming chaotic. The harmony between the colors suggests a solid understanding of color theory principles. Each color choice feels intentional and contributes to the overall aesthetic rather than competing for attention.")
        elif color_score >= 5:
            sections.append(f"The color palette contains {unique_colors} unique colors, which provides a reasonable foundation. However, the execution isn't as strong as it could be. Some colors work well together while others create uncomfortable juxtapositions. There's a sense that the creator understands basic color theory but hasn't yet mastered the nuance of applying it consistently across all elements.")
        elif color_score >= 3:
            sections.append(f"With only {unique_colors} unique colors, the palette feels limited and underdeveloped. The color choices seem somewhat arbitrary, lacking the cohesion that comes from a well-planned palette. There are moments where colors clash in ways that distract from the overall design rather than enhancing it.")
        else:
            sections.append(f"The color situation is genuinely problematic. With only {unique_colors} unique colors, there's not enough variety to create visual interest, and what colors are present don't work well together. This is a fundamental issue that needs to be addressed before anything else can be properly evaluated.")
        
        # Design completeness
        design_score = scores.get('design_completeness', 5)
        design_metrics = metrics.get('design', {})
        completeness = design_metrics.get('completeness_percentage', 0)
        
        if design_score >= 7:
            sections.append(f"Design completeness sits at {completeness}%, indicating a well-rounded skin that covers all the essential elements. The required sections are properly filled out, and several optional sections have been included as well. This thoroughness suggests a creator who understands the importance of providing a complete experience rather than cutting corners.")
        elif design_score >= 5:
            sections.append(f"At {completeness}% completeness, the skin covers the basics but leaves some gaps. Several important sections are present but could be more fully developed. The foundation is there, but it feels like the creator stopped short of really fleshing out every aspect of the design.")
        elif design_score >= 3:
            sections.append(f"Design completeness is only at {completeness}%, which means significant portions of this skin are missing or underdeveloped. This creates an unfinished feeling that undermines whatever strengths the skin might otherwise have. Users will notice the gaps, and they'll be disappointed by them.")
        else:
            sections.append(f"At {completeness}% completeness, this skin is fundamentally incomplete. Major sections are missing entirely, and what's present isn't developed enough to provide a satisfactory experience. This isn't a skin that needs refinement - it's a skin that needs to be finished.")
        
        # Animation readiness
        anim_score = scores.get('animation_readiness', 5)
        anim_metrics = metrics.get('animation', {})
        
        if anim_score >= 7:
            sections.append(f"The animation preparation is excellent. Custom animations are well-defined with appropriate timing parameters. The creator has clearly thought about how this character will move and express itself, and that forethought will pay off in the final experience.")
        elif anim_score >= 5:
            sections.append(f"Animation setup is functional but basic. The essential parameters are configured, but there's room for more detailed animation frames and custom animations that would give the character more personality and expressiveness.")
        elif anim_score >= 3:
            sections.append(f"Animation configuration is minimal. Basic parameters may be set, but without more detailed animation frames, the character will likely appear stiff and unresponsive. This is a critical area for improvement.")
        else:
            sections.append(f"Animation support is severely lacking. Without proper configuration, this character won't be able to express itself through movement, which is a fundamental requirement for a MEMEBOT skin. This needs to be addressed as a top priority.")
        
        # Customization depth
        custom_score = scores.get('customization_depth', 5)
        custom_metrics = metrics.get('customization', {})
        total_points = custom_metrics.get('total_customization_points', 0)
        
        if custom_score >= 7:
            sections.append(f"With {total_points} customization points, users have extensive control over how this character looks. The variety of options means each user can create a version that feels uniquely theirs. This level of customization depth significantly increases the skin's value and replayability.")
        elif custom_score >= 5:
            sections.append(f"The {total_points} customization points provide a decent range of options, though some areas feel more developed than others. Users will appreciate the ability to personalize, but they may wish for more control in certain aspects.")
        elif custom_score >= 3:
            sections.append(f"At {total_points} customization points, the options are limited. Users won't have much flexibility to make this character their own, which reduces the skin's long-term appeal.")
        else:
            sections.append(f"Customization is minimal with only {total_points} points of control. This severely limits the skin's versatility and will likely lead to user frustration. Expanding customization options should be a priority.")
        
        # Structural quality
        struct_score = scores.get('structural_quality', 5)
        struct_metrics = metrics.get('structural', {})
        lua_length = struct_metrics.get('lua_script_length', 0)
        data_depth = struct_metrics.get('data_depth', 0)
        
        if struct_score >= 7:
            sections.append(f"The structural quality is strong, with a Lua script of {lua_length} characters and data depth of {data_depth} levels. The skin is well-organized with proper metadata and a clean architecture that suggests the creator understands best practices for skin development.")
        elif struct_score >= 5:
            sections.append(f"Structurally, the skin is adequate but not exceptional. The Lua script is {lua_length} characters with {data_depth} levels of data depth. There's room for more sophisticated scripting and better organization of the skin data.")
        elif struct_score >= 3:
            sections.append(f"The structural foundation is weak. The Lua script is only {lua_length} characters with shallow data depth of {data_depth}. This limits what the skin can do and suggests a need for better understanding of skin architecture.")
        else:
            sections.append(f"Structural issues are severe. The Lua scripting is minimal ({lua_length} characters) and the data structure is shallow ({data_depth} levels). This skin needs to be rebuilt with proper architecture before it can function reliably.")
        
        return '\n\n'.join(sections)
    
    def _generate_emotional_reaction(self, emotional_state: str, persona: Dict,
                                    overall_score: float, strengths: List,
                                    weaknesses: List, skin_name: str) -> str:
        """Generate emotional reaction section (150-400 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 30)
        
        if emotional_state == 'toxic':
            templates = [
                f"I need to be completely honest about how {skin_name} makes me feel. It makes me feel frustrated. It makes me feel like my time as a reviewer is being disrespected. It makes me feel like the creator doesn't take this seriously, doesn't respect the platform, doesn't respect the users who will have to look at this. I'm not being hyperbolic when I say this is one of the most disappointing reviewing experiences I've had.",
                f"The emotions I'm experiencing looking at {skin_name} aren't good ones. There's irritation at the obvious shortcuts. There's anger at the wasted potential. There's a deep, profound frustration that someone thought this was ready to share with the world. I take reviewing seriously, and when I encounter work that clearly wasn't taken seriously by its creator, it genuinely upsets me.",
                f"I'm trying to remain professional, but {skin_name} is testing my patience. Every element I examine reveals another shortcut, another missed opportunity, another sign that the creator just didn't care enough. And that's what really gets me - not the lack of skill, but the apparent lack of effort. Skill can be developed. Effort is a choice."
            ]
        elif emotional_state == 'heartbreaking':
            templates = [
                f"My emotional response to {skin_name} is complicated. There's sadness, certainly - sadness that something created with such obvious hope didn't turn out the way it was supposed to. But there's also tenderness. I want to protect this creator from the harsh feedback I know they'll receive. I want to guide them gently toward improvement rather than crushing their spirit.",
                f"Looking at {skin_name}, I feel a deep sense of empathy. I remember being at this stage in my own creative journey. I remember the excitement of finishing something and the crushing disappointment when others didn't see what I saw. The creator of this skin is going through something universal, something every artist experiences, and my heart goes out to them.",
                f"There's a particular quality to {skin_name} that makes me emotional in a way most skins don't. It's the earnestness. The genuine attempt to create something beautiful, even if that attempt fell short. In a world full of cynical, calculated creations, there's something almost precious about a skin that tries so hard and misses the mark."
            ]
        elif emotional_state == 'angry':
            templates = [
                f"I want the creator of {skin_name} to understand exactly why I'm angry. I'm not angry because the skin is bad. I'm angry because it could have been good. The bones of something decent are visible beneath the mess, and instead of developing those bones into something strong, the creator just... stopped. They gave up. They decided 'good enough' was acceptable. And that decision infuriates me.",
                f"My anger about {skin_name} is the anger of someone who cares. If I didn't care about this platform, about this community, about the craft of skin creation, I wouldn't be angry. I'd just click away and forget about it. But I do care. I care deeply. And seeing work that shows so little care in return makes me furious.",
                f"The more I look at {skin_name}, the angrier I get. Not at the lack of skill - skill takes time to develop and I understand that. But at the lack of effort. At the corners that were clearly cut. At the decisions that were made out of laziness rather than creative choice. That's what I can't forgive."
            ]
        elif emotional_state == 'devastated':
            templates = [
                f"There's a heaviness in my chest as I write this review. {skin_name} has affected me in a way I wasn't expecting. I came into this review ready to analyze and critique, and instead I find myself feeling genuinely sad. Not sad for myself - sad for the creator. Sad for whatever circumstances led to this. Sad for the beautiful potential that didn't materialize.",
                f"I've been doing this long enough to know when something deeper is going on with a creator. {skin_name} isn't the work of someone who's lazy or untalented. It's the work of someone who's lost. Someone who's struggling. Someone who might be going through something that's affecting their ability to create at the level they're capable of. And that realization is devastating.",
                f"The silence after I finished examining {skin_name} was heavy. I just sat there, staring at my screen, feeling this profound sense of loss. Loss of what? Loss of what this skin could have been. Loss of the creator's confidence. Loss of the joy that creation is supposed to bring. This isn't just a bad skin. It's a cry for help."
            ]
        elif emotional_state == 'ecstatic':
            templates = [
                f"I don't use this word lightly, but {skin_name} has brought me genuine joy. Not just satisfaction at seeing good work, but actual, bubbling-up, can't-stop-smiling joy. The kind of joy that reminds you why you fell in love with something in the first place. This skin has reignited my passion for reviewing and reminded me what's possible when a creator truly gives their all.",
                f"My emotional response to {skin_name} is overwhelming in the best possible way. There's excitement at discovering something this good. There's gratitude toward the creator for putting in the work. There's anticipation at the thought of seeing what they'll create next. I feel energized, inspired, and genuinely happy.",
                f"I'm actually getting emotional writing this review because {skin_name} represents everything I love about this community. It's creative, bold, meticulously crafted, and clearly a labor of love. The creator didn't just make a skin - they poured their heart into it. And you can feel that heart in every pixel."
            ]
        elif emotional_state == 'confused':
            templates = [
                f"My dominant emotion reviewing {skin_name} is confusion. Deep, genuine confusion. I keep looking at it from different angles, trying to understand what the creator was going for. Were they being experimental? Is this irony? Is there a cultural reference I'm missing? The fact that I can't answer these questions is troubling.",
                f"There's an unsettled feeling I get from {skin_name} that I can't quite shake. It's not the comfortable confusion of avant-garde art that's intentionally challenging. It's the uncomfortable confusion of something that seems like it should make sense but doesn't. I feel like I'm missing crucial context that would make everything click into place.",
                f"I've never had a skin make me question my own judgment before, but {skin_name} has done exactly that. Am I being too harsh? Too generous? Am I even qualified to review something I so fundamentally don't understand? These are the questions running through my mind as I write this."
            ]
        else:
            templates = [
                f"My overall emotional response to {skin_name} is measured. There are aspects that impress and aspects that disappoint, and my feelings reflect that balance. I'm neither overjoyed nor distressed - I'm thoughtfully engaged with the work, considering it carefully before reaching conclusions.",
                f"Reviewing {skin_name} has been an intellectually stimulating experience. The strengths give me genuine appreciation, while the weaknesses give me concrete things to think about and suggest. This is the kind of review that reminds me why I value thorough, analytical assessment.",
                f"My feelings about {skin_name} are nuanced. I appreciate certain elements while being critical of others. This isn't a skin that evokes strong emotions in either direction - it's a skin that invites careful consideration and balanced judgment."
            ]
        
        return rng.choice(templates)
    
    def _generate_feature_breakdown(self, emotional_state: str, persona: Dict,
                                   scores: Dict, metrics: Dict, strengths: List,
                                   weaknesses: List) -> str:
        """Generate specific feature breakdown (200-500 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 40)
        
        focus_areas = persona.get('focus_areas', ['colors', 'design'])
        sections = []
        
        # Pick 3-5 specific features to break down
        features_to_analyze = rng.sample(focus_areas, min(3, len(focus_areas)))
        
        for feature in features_to_analyze:
            if feature in [s.lower() for s in strengths]:
                positive_templates = [
                    f"The {feature} is a clear strength of this skin. It's been given careful attention and it shows in the final result. Everything from the initial concept to the execution demonstrates competence and care.",
                    f"I want to highlight the {feature} specifically because it's an area where this skin genuinely excels. In a design where other elements might struggle, the {feature} stands as a testament to what the creator is capable of when they focus their efforts.",
                    f"Let me talk about the {feature} for a moment, because this is where the creator's talent really shines through. It's well-conceived, well-executed, and adds significant value to the overall skin."
                ]
                sections.append(rng.choice(positive_templates))
                
            elif feature in [w.lower() for w in weaknesses]:
                if emotional_state in ['toxic', 'angry']:
                    critical_templates = [
                        f"The {feature} is a disaster. There's no gentle way to put it. It fails at a fundamental level and drags down everything around it. This needs to be completely rethought and rebuilt.",
                        f"I don't know what happened with the {feature}, but whatever approach was taken, it was the wrong one. This is the weakest element of the skin by a significant margin and needs immediate attention.",
                        f"The {feature} makes me actively angry because of how badly it's handled. It's not just bad - it's carelessly bad. The kind of bad that comes from not even trying."
                    ]
                    sections.append(rng.choice(critical_templates))
                elif emotional_state in ['heartbreaking', 'devastated']:
                    sad_templates = [
                        f"The {feature} is where my heart breaks the most. I can see the intention, I can see what the creator wanted to achieve, but the execution just isn't there. It's so close to being good, and yet so far.",
                        f"I wish I could say the {feature} works, but it doesn't. And that's genuinely sad because you can tell the creator invested time and hope into it. The gap between aspiration and result is painful to witness.",
                        f"The {feature} makes me want to sit down with the creator and work through it together. Not because it's terrible, but because it's almost there. It needs guidance, not criticism."
                    ]
                    sections.append(rng.choice(sad_templates))
                elif emotional_state == 'confused':
                    confused_templates = [
                        f"The {feature} is where my confusion peaks. I genuinely don't understand what the creator was trying to accomplish here. The choices made seem to contradict basic principles without any apparent artistic justification.",
                        f"I keep coming back to the {feature} because it baffles me. Nothing about it makes sense in context. It's like a puzzle piece from a completely different puzzle was forced into this one.",
                        f"If someone could explain the creative reasoning behind the {feature}, I would genuinely love to hear it. Because right now, I'm completely lost."
                    ]
                    sections.append(rng.choice(confused_templates))
                else:
                    constructive_templates = [
                        f"The {feature} is an area that needs attention. It's not working as well as it could, and improvements here would significantly enhance the overall skin quality.",
                        f"I'd recommend focusing on the {feature} as a priority for improvement. It's currently one of the weaker elements and addressing it would have an outsized positive impact.",
                        f"The {feature} has room for improvement. With some focused effort, this could become a strength rather than a weakness."
                    ]
                    sections.append(rng.choice(constructive_templates))
            else:
                neutral_templates = [
                    f"The {feature} is functional but unremarkable. It does what it needs to do without drawing attention to itself, either positively or negatively.",
                    f"Regarding the {feature}, it's adequate. Not a standout element, but not a problem either. It serves its purpose in the overall design.",
                    f"The {feature} falls somewhere in the middle - competent enough to work, but not distinctive enough to be memorable."
                ]
                sections.append(rng.choice(neutral_templates))
        
        return '\n\n'.join(sections)
    
    def _generate_comparison_section(self, emotional_state: str, persona: Dict,
                                    overall_score: float, skin_name: str) -> str:
        """Generate comparison to other work (100-300 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 50)
        
        if emotional_state == 'toxic':
            templates = [
                f"I've reviewed skins made by children, by complete beginners, by people who had never used design software before. And I can honestly say that {skin_name} ranks among the most disappointing. Because those other creators had an excuse - they were learning. What's the excuse here?",
                f"In the pantheon of bad skins I've reviewed, {skin_name} doesn't even have the decency to be interestingly bad. It's just... bad. Boringly, predictably, exhaustingly bad. At least some terrible skins are memorable. This one I'll be trying to forget.",
                f"I've seen skins with half the effort and twice the quality. I've seen skins made in an afternoon that blow this out of the water. I've seen skins that made me cringe but at least made me feel something other than disappointment."
            ]
        elif emotional_state == 'heartbreaking':
            templates = [
                f"I've reviewed skins that were technically worse than {skin_name}, but none that made me sadder. Because those worse skins usually came from people who just didn't know any better. This one comes from someone who clearly does know better, or at least could know better with guidance.",
                f"The difference between {skin_name} and other skins at this quality level is the emotional weight behind it. Most mediocre skins are forgettable. This one isn't, because you can feel the creator's hopes and dreams embedded in every flawed element.",
                f"Compared to other skins I've reviewed, {skin_name} occupies a unique space. It's not the worst I've seen - not even close. But it might be the one I most wish I could fix. The one where the gap between what is and what could have been hurts the most."
            ]
        elif emotional_state == 'angry':
            templates = [
                f"I've reviewed skins that made me roll my eyes. Skins that made me sigh. Skins that made me question the future of the platform. But {skin_name} is the first skin in a long time that made me genuinely angry. Because I've seen what this creator can do, and this isn't it.",
                f"Let me compare {skin_name} to something. Imagine a chef who's cooked beautiful meals suddenly serving you burnt toast and claiming it's their best work. That's what this feels like. That's the level of disconnect between capability and output that we're dealing with here.",
                f"Other reviewers might be gentle. They might soft-pedal their criticism to spare the creator's feelings. I'm not going to do that. Because I've seen too many creators stagnate because nobody told them the truth. And the truth is, compared to what this creator should be capable of, {skin_name} is a failure."
            ]
        elif emotional_state == 'devastated':
            templates = [
                f"I keep thinking about the creator's earlier work while looking at {skin_name}. The progression from promising newcomer to this... it's heartbreaking. Something changed. Something went wrong. And I don't know what it was, but I can see the evidence of it in every compromised design choice.",
                f"There's a particular kind of tragedy in watching an artist decline. It's different from seeing a beginner struggle - that's natural, expected, even encouraging. But seeing someone who was once good produce work that's worse than what they made years ago? That's devastating.",
                f"I've followed this creator's journey, and {skin_name} represents a significant step backward. Not a stumble - stumbles are normal. This is a retreat. An abandonment of standards that were previously met. And I don't know how to process that except with sadness."
            ]
        elif emotional_state == 'ecstatic':
            templates = [
                f"I've reviewed legendary skins. Skins that people still talk about years later. Skins that set standards everyone else tried to meet. And {skin_name} belongs in that conversation. It's not just good - it's historically good. The kind of good that becomes a reference point for future reviews.",
                f"Comparing {skin_name} to other excellent skins I've reviewed, it stands out even among that elite company. There's a level of craft here that exceeds what I've come to expect even from the best creators. This is next-level work that deserves next-level recognition.",
                f"In the history of this platform, there have been maybe a dozen skins that truly changed the game. That made everyone stop and pay attention. That raised the bar for everyone else. {skin_name} is one of those skins. I'm confident saying that after reviewing thousands of submissions."
            ]
        elif emotional_state == 'confused':
            templates = [
                f"Normally when I review a skin, I can place it somewhere on the spectrum from terrible to excellent. But {skin_name} defies placement. It exists in some strange quantum state where it seems simultaneously good and bad, polished and rough, intentional and accidental.",
                f"I've reviewed confusing skins before, but {skin_name} takes confusion to a new level. Most confusing skins eventually resolve into something coherent if you study them long enough. This one doesn't. The more I study it, the more confused I become.",
                f"Comparing {skin_name} to other skins is almost impossible because I can't figure out what to compare it to. It doesn't fit neatly into any category. It's not clearly good, not clearly bad, not clearly experimental. It's just... unclear."
            ]
        else:
            templates = [
                f"In the context of the broader skin ecosystem, {skin_name} occupies a middle position. It's not breaking new ground, but it's not falling behind either. It's competent work that will appeal to users looking for something solid and reliable.",
                f"Compared to similar skins in this category, {skin_name} holds its own. It has distinct strengths that differentiate it and weaknesses that are common to the category. It's a respectable entry that contributes positively to the platform.",
                f"Looking at {skin_name} alongside its peers, it's a solid if unspectacular entry. It doesn't push boundaries or challenge conventions, but it executes competently on established formulas."
            ]
        
        return rng.choice(templates)
    
    def _generate_advice_section(self, emotional_state: str, tier: str,
                                weaknesses: List, suggestions: List,
                                persona: Dict) -> str:
        """Generate constructive advice section (100-300 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 60)
        
        if emotional_state == 'toxic':
            templates = [
                f"Here's what needs to happen. First, take {rng.choice(weaknesses) if weaknesses else 'everything'} and start over. Completely. From scratch. Don't try to salvage this - there's nothing worth saving. Second, study actual good skins. Learn what works and why. Third, don't submit anything until you can look at it and honestly say it's better than what you've done before.",
                f"My advice is simple: delete this and pretend it never happened. Then go back to basics. Learn color theory. Study anatomy. Practice your craft. Don't submit anything for review for at least three months while you actually develop some skills.",
                f"If you want to improve, here's what you do: find the best skins on this platform, the ones with the highest ratings and most positive reviews. Study them obsessively. Figure out what they do differently. Then try to replicate their quality. Not their style - their quality. Once you can match that, then you can develop your own style."
            ]
        elif emotional_state == 'heartbreaking':
            templates = [
                f"Here's my advice, and I give it with love. Take a step back. Give yourself some distance from {skin_name}. Then come back and look at it with fresh eyes. I think you'll see what I'm seeing. And once you do, I want you to know that it's okay. Every creator goes through this. The important thing is to keep going.",
                f"You have the vision. I can see it clearly. What you need now is to develop the technical skills to match that vision. That takes time and practice. Be patient with yourself. Study the fundamentals. Practice deliberately. And most importantly, don't give up.",
                f"My advice comes from a place of genuine care. Find a mentor if you can. Someone whose work you admire who's willing to give you honest feedback. Having someone guide you through the rough patches can make all the difference. And please, keep creating. Your voice matters, even when the execution falls short."
            ]
        elif emotional_state == 'angry':
            templates = [
                f"Here's what I need you to do. Take responsibility for this. Don't make excuses. Don't blame lack of time or resources. Own the fact that you submitted work that wasn't ready. Then make a commitment to yourself that you'll never do that again. You owe it to yourself and to this community.",
                f"My advice: raise your standards. Drastically. Whatever bar you set for yourself before submitting this, triple it. You're capable of better. I know you are. Now you need to know it too and act like it.",
                f"Stop cutting corners. Stop settling. Stop submitting work that you know deep down isn't ready. Every time you do that, you're telling yourself that mediocrity is acceptable. It's not. Demand more from yourself."
            ]
        elif emotional_state == 'devastated':
            templates = [
                f"If you're going through something, please reach out for help. Creative block, burnout, personal struggles - these are real and they affect your work. There's no shame in taking a break, in asking for support, in admitting that you're not okay. Your wellbeing matters more than any skin.",
                f"Take the time you need. Step away if you have to. The platform will still be here when you're ready to return. And when you do return, I hope you'll come back with renewed energy and passion. You've done good work before. You can do it again.",
                f"My advice is less about the skin and more about you as a creator. Something is off. I can see it in your work. Address whatever that something is before you try to create again. You can't pour from an empty cup."
            ]
        elif emotional_state == 'ecstatic':
            templates = [
                f"My advice? Keep doing exactly what you're doing. Whatever your process is, whatever inspired this level of quality, bottle it and use it forever. You've found something special here. Nurture it. Protect it. Don't let anyone convince you to compromise your vision.",
                f"At this level, advice becomes about refinement rather than correction. So here's my refinement suggestion: {rng.choice(suggestions) if suggestions else 'keep pushing the boundaries of what you think is possible'}. That's it. That's all I've got. You're operating at a level where I can only suggest subtle improvements.",
                f"The only advice I can give someone operating at this level is to stay hungry. Don't get complacent. Don't assume you've figured everything out. The moment you stop pushing yourself is the moment your work starts declining. Stay curious, stay humble, stay hungry."
            ]
        elif emotional_state == 'confused':
            templates = [
                f"My advice is to clarify your vision before you do anything else. What exactly are you trying to achieve with this skin? What feeling do you want users to have? What makes this skin unique? If you can't answer these questions clearly, that's the first problem to solve.",
                f"Before you make any technical changes, sit down and write out your design philosophy for this skin. What's the core concept? Who's the target user? What's the emotional tone? Once you have clear answers, use them as a filter for every design decision.",
                f"Get feedback from people who will be honest with you. Show them the skin and ask them to describe what they think it's supposed to be. If their answers don't match your intention, you've got a communication problem that needs solving before anything else."
            ]
        else:
            templates = [
                f"Focus on the fundamentals. {rng.choice(suggestions) if suggestions else 'Continue developing all aspects of the skin evenly'}. Consistent improvement across all areas will yield better results than trying to make one element perfect while neglecting others.",
                f"Prioritize the changes that will have the biggest impact. {rng.choice(weaknesses) if weaknesses else 'The areas I have noted for improvement'} should be addressed first, as they're currently holding the skin back the most.",
                f"Set specific, measurable goals for improvement. Rather than 'make it better,' target specific metrics like increasing color variety or adding more customization options. Concrete goals lead to concrete results."
            ]
        
        return rng.choice(templates)
    
    def _generate_future_outlook(self, emotional_state: str, persona: Dict,
                                overall_score: float, skin_name: str) -> str:
        """Generate future outlook section (100-200 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 70)
        
        if emotional_state == 'toxic':
            templates = [
                f"The future for {skin_name} looks bleak unless dramatic changes are made. And I mean dramatic - not tweaks, not adjustments, but fundamental rethinking of every design decision. Without that level of commitment to improvement, this skin will deservedly fade into obscurity.",
                f"I don't see a path forward for {skin_name} in its current form. The issues are too numerous and too fundamental. A complete rebuild is the only option, and I'm not confident that will happen based on what I'm seeing here.",
                f"Unless the creator undergoes a complete transformation in their approach to quality, I predict {skin_name} will be forgotten within weeks. There's nothing here to sustain user interest, nothing to encourage repeat usage, nothing to build a reputation on."
            ]
        elif emotional_state == 'heartbreaking':
            templates = [
                f"I believe in this creator's future, even if {skin_name} isn't the breakthrough they hoped for. The talent is there, buried beneath the mistakes. With time, practice, and guidance, I truly believe they can create something beautiful. This isn't the end of their story.",
                f"The future I see for this creator is bright, but it might not include {skin_name}. Sometimes the best thing you can do with a project is let it go and start fresh with the lessons you've learned. I hope the creator takes those lessons and creates something worthy of their potential.",
                f"Looking ahead, I have hope. Not for this skin in particular, but for the person who made it. Because the desire to create, the willingness to put yourself out there - that's the hard part. The technical skills can be learned. The creative vision can be developed. Don't lose that spark."
            ]
        elif emotional_state == 'angry':
            templates = [
                f"The future of {skin_name} depends entirely on whether the creator is willing to put in the work they've been avoiding. If they step up, take this seriously, and commit to real improvement, there's a path forward. If they continue cutting corners, this skin has no future at all.",
                f"I want to see this creator succeed. That's why I'm so angry - because I know they can do better. The future is entirely in their hands. They can either use this feedback as fuel to improve, or they can ignore it and stay exactly where they are. The choice is theirs.",
                f"Predicting the future is easy when you've seen as many creators as I have. Those who take harsh feedback seriously improve. Those who make excuses don't. Which category this creator falls into will determine whether {skin_name} becomes a stepping stone or a tombstone."
            ]
        elif emotional_state == 'devastated':
            templates = [
                f"I worry about the future. Not for {skin_name} - that's just a skin. I worry about the creator. The trajectory I'm seeing is concerning, and without intervention, it may continue downward. I hope they have support. I hope they have people who care about them and their art.",
                f"The future is uncertain. Creators have come back from worse declines than this, but they've also disappeared entirely. I hope this creator finds their way back. I hope {skin_name} becomes a turning point rather than an ending point.",
                f"If the creator can address whatever is affecting their work, there's hope for the future. The talent didn't disappear - it's just buried under something. Dig it out. Rediscover what made you love creating in the first place. The future can still be bright."
            ]
        elif emotional_state == 'ecstatic':
            templates = [
                f"The future for {skin_name} is blindingly bright. This is going to become one of the most popular skins on the platform. I'm confident in that prediction. The quality is undeniable, and users will recognize it. The creator should prepare for a lot of attention.",
                f"I'm genuinely excited to see what this creator does next. If {skin_name} is any indication, we're witnessing the emergence of a major talent. I'll be following their work closely and I expect great things in the future.",
                f"The trajectory is clear: this creator is going places. {skin_name} will be remembered as a breakthrough moment, the skin that announced a major talent to the world. I feel privileged to have reviewed it at this early stage."
            ]
        elif emotional_state == 'confused':
            templates = [
                f"The future of {skin_name} depends on clarification. If the creator can articulate a clear vision and execute it consistently, there's potential here. If the confusion continues, users will move on to skins that communicate more clearly.",
                f"I can't predict the future of something I don't fully understand. {skin_name} could go either way - it could be refined into something coherent, or it could remain a confusing puzzle that users can't connect with. The creator's next moves will be crucial.",
                f"The uncertainty around {skin_name} makes forecasting difficult. I've seen confusing skins become cult favorites and I've seen them disappear without a trace. The difference usually comes down to whether the creator can channel whatever they're trying to express into a more accessible form."
            ]
        else:
            templates = [
                f"With continued development, {skin_name} has the potential to grow its user base and improve its standing. The foundation is solid, and incremental improvements will compound over time into significant quality gains.",
                f"The future trajectory will depend on how the creator responds to feedback. If they address the identified weaknesses while building on the strengths, {skin_name} could become a strong contender in its category.",
                f"Looking ahead, I see steady growth for {skin_name} if the creator maintains their current level of effort and continues to refine the design. Consistency is key - keep showing up, keep improving, keep caring about the work."
            ]
        
        return rng.choice(templates)
    
    def _generate_emotional_conclusion(self, emotional_state: str, tier: str,
                                      persona: Dict, overall_score: float,
                                      skin_name: str) -> str:
        """Generate emotional conclusion (100-300 words)"""
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 80)
        
        if emotional_state == 'toxic':
            pool = TOXIC_CONCLUSIONS
        elif emotional_state == 'heartbreaking':
            pool = HEARTBREAKING_CONCLUSIONS
        elif emotional_state == 'angry':
            pool = ANGRY_CONCLUSIONS
        elif emotional_state == 'devastated':
            pool = DEVASTATED_CONCLUSIONS
        elif emotional_state == 'ecstatic':
            pool = ECSTATIC_CONCLUSIONS
        elif emotional_state == 'confused':
            pool = CONFUSED_CONCLUSIONS
        else:
            pool = CONCLUSION_PHRASES
        
        base_conclusion = rng.choice(pool)
        
        # Add rating-based emphasis
        if overall_score >= 9.0:
            base_conclusion += " This is truly exceptional work that deserves the highest recognition."
        elif overall_score >= 7.0:
            base_conclusion += " Solid work that I'm happy to recommend to others."
        elif overall_score >= 5.0:
            base_conclusion += " There's work to be done, but the foundation is there."
        elif overall_score >= 3.0:
            base_conclusion += " Significant improvement is needed before this can be considered ready."
        else:
            base_conclusion += " This requires fundamental rethinking and substantial revision."
        
        return base_conclusion
    
    def _generate_ai_disclaimer(self, persona: Dict, emotional_state: str) -> str:
        """Generate AI disclaimer with emotional context"""
        bot_name = persona.get('name', 'Bot')
        
        disclaimers = [
            f"🤖 {bot_name} is an AI reviewer providing honest, algorithmically-generated feedback based on skin analysis. This review reflects my {emotional_state} assessment of the skin's objective qualities. I am not a real person, but I give my very best analysis to help creators improve their work.",
            f"⚡ {bot_name} here. I'm an AI bot programmed to analyze skins and express my findings with genuine emotional depth. While my emotions are simulated, my analysis is based on real metrics and design principles. I always give my very best review.",
            f"💡 {bot_name} | AI Reviewer: This review represents my algorithmic assessment delivered with {emotional_state} emotional tone. I analyze colors, design, animations, and structure to provide comprehensive feedback. I give my very best evaluation every time.",
            f"🎯 {bot_name} - AI Review System: I combine objective skin analysis with emotionally expressive delivery to provide meaningful feedback. My {emotional_state} tone reflects the quality of the work, and my assessment is based on thorough algorithmic evaluation."
        ]
        
        rng = random.Random(self.review_count * 7919 + persona.get('bot_index', 0) + 90)
        return rng.choice(disclaimers)
    
    def generate_organic_engagement(self, days_elapsed: float, skin_quality: float) -> Dict:
        """Generate realistic organic engagement metrics based on time elapsed"""
        
        rng = random.Random(int(days_elapsed * 1000) + int(skin_quality * 100))
        
        total_views = 0
        for day in range(1, int(days_elapsed) + 1):
            total_views += self.get_views_for_day(day, skin_quality)
        
        partial_day = days_elapsed - int(days_elapsed)
        if partial_day > 0:
            total_views += int(self.get_views_for_day(days_elapsed, skin_quality) * partial_day)
        
        total_likes = 0
        for day in range(1, int(days_elapsed) + 1):
            daily_views = self.get_views_for_day(day, skin_quality)
            total_likes += self.get_likes_for_views(daily_views, skin_quality, day)
        
        share_rate = rng.uniform(0.05, 0.15)
        total_shares = int(total_likes * share_rate)
        
        save_rate = rng.uniform(0.1, 0.3)
        total_saves = int(total_likes * save_rate)
        
        total_comments = self.get_available_bot_count(days_elapsed)
        
        return {
            'views': total_views,
            'likes': total_likes,
            'shares': total_shares,
            'saves': total_saves,
            'comments_count': total_comments,
            'days_elapsed': round(days_elapsed, 1),
            'hourly_view_rate': round(total_views / max(1, days_elapsed * 24), 2),
            'engagement_rate': round(
                (total_likes + total_comments + total_shares + total_saves) / max(1, total_views), 
                3
            )
        }
    
    def get_next_bot_to_review(self, days_elapsed: float) -> Optional[Dict]:
        """Get the next bot that should review based on organic discovery"""
        if not self.submission_start_time:
            self.submission_start_time = datetime.now()
            days_elapsed = 0
        
        expected_bots = self.get_available_bot_count(days_elapsed)
        
        if len(self.bots_reviewed) >= expected_bots:
            return None
        
        for i in range(self.total_bots_available):
            if i not in self.bots_reviewed:
                return get_bot_persona(i)
        
        return None
    
    def clear_history(self):
        """Clear review history and reset state"""
        self.review_history = []
        self.used_phrases = set()
        self.review_count = 0
        self.bots_reviewed = set()
        self.submission_start_time = None
        self.global_phrase_tracker = {}