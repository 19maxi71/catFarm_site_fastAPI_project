from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.colors import pink, black
from io import BytesIO
import os


def create_contract_pdf():
    """Generate PDF version of the sales contract."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center
        textColor=pink
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        alignment=1,  # Center
    )

    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.leading = 14

    bold_style = ParagraphStyle(
        'Bold',
        parent=normal_style,
        fontName='Helvetica-Bold'
    )

    # Content
    story = []

    # Title
    story.append(Paragraph("LavanderCats", title_style))
    story.append(Paragraph("Kitten Sales Contract", subtitle_style))
    story.append(Spacer(1, 12))

    # Introduction
    intro_text = """
    A contract must be signed &amp; notarized before purchasing our Siberian kittens. This contract is designed to protect the buyer, the seller and the welfare of the Siberian kitten. Please take this contract to your veterinarian's office with the kitten so they are aware of the contract agreement.
    """
    story.append(Paragraph(intro_text, normal_style))
    story.append(Spacer(1, 12))

    # Seller/Buyer section
    story.append(Paragraph("<b>Seller:</b> Oresta Koshyk", normal_style))
    story.append(
        Paragraph("<b>Buyer:</b> ____________________________", normal_style))
    story.append(Spacer(1, 12))

    # Description
    story.append(Paragraph("<b>Description of Kitten:</b>", bold_style))
    story.append(Paragraph("Name: ___________________", normal_style))
    story.append(Paragraph("Breed: Siberian", normal_style))
    story.append(
        Paragraph("Color/Pattern: ____________________", normal_style))
    story.append(Paragraph("Date of Birth: ________________", normal_style))
    story.append(Paragraph("Sex: ________________", normal_style))
    story.append(Paragraph("Purchase Amount: ________________", normal_style))
    story.append(Paragraph("Microchip #: ________________", normal_style))
    story.append(Spacer(1, 12))

    # Conditions
    story.append(Paragraph("<b>Condition of the Sale</b>", bold_style))
    conditions = [
        "1. The Seller guarantees that this kitten is healthy to the best of their knowledge, that the kitten will have been examined by a licensed veterinarian and is currently on vaccinations.",
        "2. The Buyer is advised to take the kitten to the vet for a health exam within 72 hours; if any health concerns are found, the Buyer may return the kitten to the seller within 72 hours with a written explanation from the attending vet, for a full refund or exchange upon availability of a kitten. No medical or travel charges will be refunded.",
        "3. During the first 72 hours kittens should be isolated from any other pets and monitored for health, eating, litter box usage, and activity level. The Seller is not responsible for any injury or illness to other pets caused by exposure to this kitten.",
        "4. Due to the controversy of the FELV/FIV vaccine we recommend that this vaccine should NOT be given to our kittens as they are not outdoor cats and should not encounter this. Our cats are not to be left outdoors, nor should they be exposed to cats with FELV/FIV.",
        "5. Whenever a vaccine is being administered, only ONE vaccine should be given at a time. Seller doesn't guarantee kittens wellbeing due to adverse reactions to future vaccinations.",
        "6. The Seller guarantees the kitten described above is free of FELV (Feline Leukemia) and FIV (Feline AIDS) at the time of shipment, pick-up or delivery. One kitten from each litter will have been tested for FELV/FIV."
    ]

    for condition in conditions:
        story.append(Paragraph(condition, normal_style))
        story.append(Spacer(1, 6))

    # Additional terms (abbreviated for PDF)
    additional_terms = [
        "7. This kitten is not to be declawed under ANY circumstances. The Buyer will be pay fine of $5,000.00 if any kitten bought from LavanderCats cattery will be declawed.",
        "8. Under no circumstances will this kitten be sold, leased or given away to any pet store, research laboratory, breeding mill or similar facility. If you can no longer keep this kitten, you MUST contact the Seller.",
        "9. If this kitten dies of FIP it will be replaced if FIP virus RealPCR test (code 3630) is performed on peritoneal fluid, pleural fluid, CFF, tissue biopsy, or aspirate.",
        "10. All our Siberian kittens are guaranteed for 2 (two) years against genetic defects, in particular and specifically HCM (hypertrophic cardiomyopathy) and PKD.",
        "16. This kitten must be altered prior to 6 months of age and proof of alteration must be submitted to the Seller.",
        "17. The Buyer must be 18 years of age or older... Deposits are non-refundable and are meant to hold a kitten for you. Final payment of the balance is in CASH only; no exceptions will be made."
    ]

    for term in additional_terms:
        story.append(Paragraph(term, normal_style))
        story.append(Spacer(1, 6))

    # Signature section
    story.append(Spacer(1, 24))
    story.append(Paragraph(
        "Signature of Purchaser: ____________________________", normal_style))
    story.append(Paragraph("Date: ____________________________", normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


def create_departure_instructions_pdf():
    """Generate PDF version of departure instructions."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        alignment=1,  # Center
        textColor=pink
    )

    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading3'],
        fontSize=14,
        spaceAfter=10,
        textColor=pink
    )

    normal_style = styles['Normal']
    normal_style.fontSize = 11
    normal_style.leading = 13

    # Content
    story = []

    # Title
    story.append(Paragraph("DEPARTURE INSTRUCTIONS", title_style))
    story.append(
        Paragraph("Welcome to the Siberian cat world!", styles['Heading2']))
    story.append(
        Paragraph("Congratulations on the new family member!", styles['Heading3']))
    story.append(Spacer(1, 12))

    # Introduction
    intro = """
    This guide covers key topics and answers common questions for the coming weeks and months. For any questions, text me at 267-538-8590 or call in an emergency. While we previously met families in person to discuss all concerns and get acquainted, we've adapted to changing times.
    """
    story.append(Paragraph(intro, normal_style))
    story.append(Spacer(1, 12))

    # Safe Heaven
    story.append(Paragraph("SAFE HEAVEN", section_style))
    safe_heaven = """
    When bringing home a new kitten, expect it to be nervous and miss its mother and siblings. Please provide a towel for sleeping, plus food, water, and a litter box.

    To help the kitten adjust, place it in your smallest room (the smaller the better) with food and water SEPARATED from the litter box. After an hour, you may enter, play with, and hold the kitten; keep it in your arms to build trust rather than letting it roam.

    After one hour, return the kitten to the litter box and close the door. Allow approximately 15 minutes before repeating this process.

    By the third day, the kitten should begin seeking your attention. At this stage, you may open the door and permit the kitten to explore independently; it has already been learned how to return to the litter box when necessary.

    Once the kitten has adjusted to its new environment and you prefer not to keep a litter box in your bathroom, purchase an additional box and place it in the designated permanent area. Keep the original box in its current location for about a month to ensure the kitten consistently uses the new box.
    """
    story.append(Paragraph(safe_heaven, normal_style))
    story.append(Spacer(1, 12))

    # Nibbling
    story.append(Paragraph("NIBBLING", section_style))
    nibbling = """
    Nibbling should not be permitted. If redirecting your kitten to a toy is ineffective, it may be appropriate to gently scruff the kitten, lift it by the scruff, firmly say "NO!", place the kitten on the floor, and then ignore it for a while.

    While nibbling may not cause harm now, kittens eventually mature and will develop stronger hunting behaviors. Then nibbling won't be so cute anymore. Cats love attention, so if you teach them there is a consequence for their naughty behavior, they will soon learn.

    It is important NOT TO PICK UP YOUR CAT BY THE SCRUFF ONCE IT IS OLDER THAN EIGHT (8) MONTHS. Teach it the basics while it's little.
    """
    story.append(Paragraph(nibbling, normal_style))
    story.append(Spacer(1, 12))

    # Bathing
    story.append(Paragraph("BATHING", section_style))
    bathing = """
    You can bathe your kitten, but I suggest wiping them with a wet towel. Gently rub the cat down with the damp towel, taking away the surface dander that causes the allergies.

    Some cat owners prefer to buy wipes in a pet store, but, honestly, they have nothing special in them (producers cannot put anything on them because it will harm a cat when it licks its fur). Give a small treat after you wipe your kitten and after 2nd bath they will look forward to it.
    """
    story.append(Paragraph(bathing, normal_style))
    story.append(Spacer(1, 12))

    # Food
    story.append(Paragraph("FOOD", section_style))
    food = """
    Feed your kitten 3 times a day. I recommend Royal Canin Mother & Baby cat food for kittens. It is very high quality and has all the nutrients they need. You can buy it at Petco or online.

    Do not give your kitten cow's milk. It will cause diarrhea. If you want to give milk, buy cat milk from the pet store.

    Do not give people food. It can cause serious health issues. No chocolate, onions, garlic, grapes, raisins, etc.

    Fresh water should always be available. Change it daily.
    """
    story.append(Paragraph(food, normal_style))
    story.append(Spacer(1, 12))

    # Other sections (abbreviated for space)
    sections = [
        ("LITTER BOX", "Use clumping litter. Clean the box daily. If you have multiple cats, have multiple boxes. If your kitten has accidents outside the box, clean it thoroughly with enzymatic cleaner."),
        ("SCRATCHING", "Provide scratching posts. Cats need to scratch to keep their claws healthy. Keep claws trimmed."),
        ("PLAYTIME", "Kittens need lots of playtime. Play with interactive toys like laser pointers and feather wands."),
        ("VETERINARIAN", "Take your kitten to the vet within 72 hours. Discuss spaying/neutering. Regular check-ups are important."),
        ("BEHAVIOR", "Kittens are curious and will get into everything. Some kittens are more active than others."),
        ("HEALTH CONCERNS", "Watch for signs of illness. Contact vet immediately if you notice any concerning symptoms.")
    ]

    for section_title, section_content in sections:
        story.append(Paragraph(section_title, section_style))
        story.append(Paragraph(section_content, normal_style))
        story.append(Spacer(1, 8))

    # Contact info
    story.append(Paragraph("CONTACT INFORMATION", section_style))
    contact = """
    For questions or concerns: Text 267-538-8590
    Emergency situations: Call your local emergency vet
    """
    story.append(Paragraph(contact, normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
