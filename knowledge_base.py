


# knowledge_base.py

disease_info = {
    # =========================================================================
    # 1. MAIZE (Cereals & Grains)
    # =========================================================================
    "maize_fall_armyworm": {
        "cause": "Insect pest Spodoptera frugiperda.",
        "treatment": ["Apply insecticides.", "Use pheromone traps."],
        "prevention": ["Plant resistant varieties.", "Practice intercropping."]
    },
    "maize_grasshopper": {
        "cause": "Various species of grasshoppers.",
        "treatment": ["Apply insecticides."],
        "prevention": ["Encourage natural predators."]
    },
    "maize_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Maintain good agricultural practices."]
    },
    "maize_leaf_beetle": {
        "cause": "Insect pest, e.g., Diabrotica spp.",
        "treatment": ["Apply insecticides."],
        "prevention": ["Practice crop rotation."]
    },
    "maize_leaf_blight": {
        "cause": "Fungus Exserohilum turcicum (Northern Leaf Blight) or Bipolaris maydis (Southern Leaf Blight).",
        "treatment": ["Apply fungicides."],
        "prevention": ["Plant resistant hybrids.", "Practice crop rotation and tillage."]
    },
    "maize_leaf_spot": {
        "cause": "Fungus Cercospora zeae-maydis (Gray Leaf Spot).",
        "treatment": ["Apply fungicides."],
        "prevention": ["Plant resistant hybrids.", "Manage crop residue."]
    },
    "maize_streak_virus": {
        "cause": "Maize streak virus (MSV).",
        "treatment": ["No cure. Remove infected plants."],
        "prevention": ["Plant resistant varieties.", "Control leafhopper vectors."]
    },

    # =========================================================================
    # 2. RICE (Cereals & Grains)
    # =========================================================================
    "rice_bacterial_leaf_blight": {
        "cause": "Caused by the bacterium Xanthomonas oryzae pv. oryzae.",
        "treatment": [
            "Application of copper-based bactericides.",
            "Use of antibiotics like streptomycin, though resistance can be an issue."
        ],
        "prevention": [
            "Planting resistant varieties of rice.",
            "Ensuring proper field sanitation by removing infected stubble and weeds.",
            "Avoiding excessive nitrogen fertilization."
        ]
    },
    "rice_brown_spot": {
        "cause": "Fungus Bipolaris oryzae (previously known as Helminthosporium oryzae).",
        "treatment": [
            "Fungicidal sprays containing propiconazole, azoxystrobin, or mancozeb can be effective.",
            "Seed treatment with fungicides before planting."
        ],
        "prevention": [
            "Use of certified disease-free seeds.",
            "Proper water management to avoid water stress.",
            "Balanced nutrient application, particularly potassium."
        ]
    },
    "healthy_rice_leaf": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": [
            "Maintain good agricultural practices.",
            "Monitor plants regularly for any signs of stress or disease."
        ]
    },
    "rice_leaf_blast": {
        "cause": "Fungus Magnaporthe oryzae (also known as Pyricularia oryzae).",
        "treatment": [
            "Application of fungicides such as tricyclazole, azoxystrobin, or kasugamycin.",
            "Silicon fertilizers can enhance plant resistance."
        ],
        "prevention": [
            "Planting resistant cultivars.",
            "Managing water levels to avoid drought stress.",
            "Avoiding excessive nitrogen application."
        ]
    },
    "rice_leaf_scald": {
        "cause": "Fungus Microdochium oryzae (previously known as Rhynchosporium oryzae).",
        "treatment": [
            "Fungicides containing propiconazole or other triazoles can be effective.",
            "Removing and destroying infected leaves."
        ],
        "prevention": [
            "Use of resistant varieties.",
            "Proper field drainage to reduce humidity.",
            "Balanced fertilization."
        ]
    },
    "rice_narrow_brown_leaf_spot": {
        "cause": "Fungus Cercospora janseana (also known as Sphaerulina oryzina).",
        "treatment": [
            "Fungicidal sprays with active ingredients like azoxystrobin or propiconazole.",
            "Application of potassium and phosphorus can reduce severity."
        ],
        "prevention": [
            "Planting resistant varieties.",
            "Good field sanitation and removal of crop residues.",
            "Maintaining optimal nutrient levels in the soil."
        ]
    },
    "rice_hispa": {
        "cause": "Insect pest Dicladispa armigera, a small, black, spiny beetle.",
        "treatment": [
            "Application of insecticides such as fipronil, chlorpyrifos, or lambda-cyhalothrin.",
            "In severe cases, manual removal of beetles can help."
        ],
        "prevention": [
            "Flooding the fields to dislodge the beetles.",
            "Encouraging natural predators like spiders and dragonflies.",
            "Synchronous planting in a region to break the pest's life cycle."
        ]
    },
    "rice_sheath_blight": {
        "cause": "Fungus Rhizoctonia solani.",
        "treatment": [
            "Application of fungicides like azoxystrobin, propiconazole, or validamycin.",
            "Foliar sprays at the first sign of disease."
        ],
        "prevention": [
            "Use of resistant varieties.",
            "Maintaining appropriate plant spacing for better air circulation.",
            "Avoiding excessive nitrogen fertilization."
        ]
    },

    # =========================================================================
    # 3. CASSAVA (Roots & Tubers)
    # =========================================================================
    "cassava_bacterial_blight": {
        "cause": "Bacterium Xanthomonas axonopodis pv. manihotis.",
        "treatment": ["No effective chemical treatment. Remove and burn infected plants."],
        "prevention": ["Use certified disease-free planting materials.", "Practice crop rotation."]
    },
    "cassava_brown_spot": {
        "cause": "Fungus Cercosporidium henningsii.",
        "treatment": ["Apply fungicides if infection is severe."],
        "prevention": ["Plant resistant varieties.", "Maintain good field sanitation."]
    },
    "cassava_green_mite": {
        "cause": "Mite Mononychellus tanajoa.",
        "treatment": ["Apply miticides.", "Use biological control agents."],
        "prevention": ["Plant resistant varieties.", "Maintain high humidity."]
    },
    "cassava_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Maintain good agricultural practices."]
    },
    "cassava_mosaic": {
        "cause": "Cassava mosaic virus (CMV).",
        "treatment": ["No cure. Remove and destroy infected plants."],
        "prevention": ["Use virus-free planting materials.", "Control whitefly vectors."]
    },

    # =========================================================================
    # 4. YAM (Roots & Tubers)
    # =========================================================================
    "yam_mosaic_virus": {
        "cause": "Yam Mosaic Virus (YMV), vector-transmitted by aphids.",
        "treatment": ["No chemical solution for the virus. Roguing and discarding vector nests is necessary."],
        "prevention": [
            "Select healthy, smooth-skinned seed tubers from strong parent vines.",
            "Maintain zero-weed field configurations to eliminate vector host spaces."
        ]
    },
    "yam_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Select clean seed tubers and ensure proper mounding with mulch protection."]
    },

    # =========================================================================
    # 5. COCOA (Cash Crops)
    # =========================================================================
    "cocoa_black_pod": {
        "cause": "Fungus Phytophthora megakarya, highly destructive in Ghana.",
        "treatment": [
            "Apply approved copper-based protectant fungicides.",
            "Remove and safely bury infected pods weekly to avoid rain splash spread."
        ],
        "prevention": [
            "Prune branches systematically to lower humidity and let in sunlight.",
            "Maintain clean row weeding to clear alternative spores."
        ]
    },
    "cocoa_swollen_shoot": {
        "cause": "Cocoa Swollen Shoot Virus (CSSV), spread by mealybugs.",
        "treatment": ["No chemical cure exists. Infected trees must be cut out completely under COCOBOD guidelines."],
        "prevention": [
            "Replant with CSSV-tolerant hybrid seed options from CRIG.",
            "Manage attendant ant nests that guard and transport vector mealybugs."
        ]
    },
    "cocoa_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Follow standard pruning schedules and clear mistletoe or parasitic epiphytes promptly."]
    },

    # =========================================================================
    # 6. PLANTAIN (Cash Crops)
    # =========================================================================
    "plantain_sigatoka": {
        "cause": "Fungus Mycosphaerella fijiensis (Black Sigatoka Leaf Streak).",
        "treatment": [
            "Apply early-stage triazole or systemic strobilurin protective sprays.",
            "Manually strip and burn heavily affected leaves."
        ],
        "prevention": [
            "Avoid dense planting; maintain a clear 3m x 3m matrix layout.",
            "Ensure proper field drainage away from root mats."
        ]
    },
    "plantain_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["De-sucker plants regularly to focus nutrient allocation on the main pseudostem crop."]
    },

    # =========================================================================
    # 7. TOMATOES (Vegetables)
    # =========================================================================
    "tomato___bacterial_spot": {
        "cause": "Bacteria Xanthomonas spp.",
        "treatment": ["Apply copper-based bactericides."],
        "prevention": ["Use disease-free seeds.", "Practice crop rotation.", "Avoid overhead watering."]
    },
    "tomato___early_blight": {
        "cause": "Fungus Alternaria solani.",
        "treatment": ["Apply fungicides containing chlorothalonil or mancozeb."],
        "prevention": ["Use resistant varieties.", "Stake plants.", "Water at the base."]
    },
    "tomato___healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Maintain good agricultural practices."]
    },
    "tomato___late_blight": {
        "cause": "Oomycete Phytophthora infestans.",
        "treatment": ["Apply fungicides proactively.", "Remove and destroy infected plants immediately."],
        "prevention": ["Use resistant varieties.", "Ensure good air circulation.", "Avoid overhead watering."]
    },
    "tomato___leaf_mold": {
        "cause": "Fungus Passalora fulva.",
        "treatment": ["Apply fungicides.", "Improve air circulation."],
        "prevention": ["Use resistant varieties.", "Reduce humidity.", "Stake plants."]
    },
    "tomato___septoria_leaf_spot": {
        "cause": "Fungus Septoria lycopersici.",
        "treatment": ["Apply fungicides containing chlorothalonil or copper."],
        "prevention": ["Practice crop rotation.", "Remove lower leaves.", "Improve air circulation."]
    },
    "tomato___spider_mites_two-spotted_spider_mite": {
        "cause": "Mite Tetranychus urticae.",
        "treatment": ["Apply miticides or insecticidal soaps.", "Introduce predatory mites."],
        "prevention": ["Keep plants well-watered.", "Increase humidity.", "Regularly inspect leaves."]
    },
    "tomato___target_spot": {
        "cause": "Fungus Corynespora cassiicola.",
        "treatment": ["Apply fungicides."],
        "prevention": ["Improve air circulation.", "Avoid overhead irrigation.", "Remove crop debris."]
    },
    "tomato___tomato_mosaic_virus": {
        "cause": "Tomato Mosaic Virus (ToMV).",
        "treatment": ["No cure. Remove and destroy infected plants."],
        "prevention": ["Use resistant varieties.", "Wash hands and tools.", "Avoid tobacco use near plants."]
    },
    "tomato___tomato_yellow_leaf_curl_virus": {
        "cause": "Tomato Yellow Leaf Curl Virus (TYLCV).",
        "treatment": ["No cure. Remove and destroy infected plants."],
        "prevention": ["Use resistant varieties.", "Control whitefly vectors.", "Use insect-proof nets."]
    },

    # =========================================================================
    # 8. PEPPERS (Vegetables)
    # =========================================================================
    "pepper_veinal_mottle": {
        "cause": "Pepper Veinal Mottle Virus (PVMV).",
        "treatment": ["No cure. Immediately isolate, pull, and burn infected pepper plants."],
        "prevention": [
            "Control aphid populations using biological sprays or protective netting.",
            "Refrain from planting near old solanaceous plots."
        ]
    },
    "pepper_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Maintain clean weeding regimes and apply balanced NPK applications."]
    },

    # =========================================================================
    # 9. ONIONS (Vegetables)
    # =========================================================================
    "onion_purple_blotch": {
        "cause": "Fungus Alternaria porri.",
        "treatment": ["Apply protective fungicidal treatments containing copper or mancozeb."],
        "prevention": [
            "Ensure field soil structure drains standing water immediately.",
            "Avoid multi-year concurrent cultivation of onions on identical blocks."
        ]
    },
    "onion_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Ensure optimal soil drainage drainage beds and clear weeds around bulbs manually."]
    },

    # =========================================================================
    # 10. BEANS (Legumes)
    # =========================================================================
    "bean_anthracnose": {
        "cause": "Fungus Colletotrichum lindemuthianum, thriving in cool, wet environments.",
        "treatment": [
            "Apply approved systemic or protectant fungicides containing mancozeb or copper oxides.",
            "Remove and destroy severely affected crop residues post-harvest."
        ],
        "prevention": [
            "Use certified disease-free bean seeds.",
            "Avoid working in or moving through bean fields when the foliage is wet to stop spore transfer."
        ]
    },
    "bean_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Keep up regular weeding and check pod configurations during growth cycles."]
    },

    # =========================================================================
    # 11. GROUNDNUTS (Legumes)
    # =========================================================================
    "groundnut_rosette": {
        "cause": "Groundnut Rosette Virus complex, managed by aphid lines.",
        "treatment": ["Uproot plants displaying severe chlorotic stunting or mottling symptoms."],
        "prevention": [
            "Sow seeds closely together to create early canopy closure, which deters incoming aphids.",
            "Utilize rosette-resistant seeds developed by local research institutes."
        ]
    },
    "groundnut_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Follow proper spacing guidelines to allow fast canopy cover closure and weed inhibition."]
    },

    # =========================================================================
    # 12. SWEET POTATO (Roots & Tubers)
    # =========================================================================
    "sweet_potato_feathery_mottle": {
        "cause": "Sweet Potato Feathery Mottle Virus (SPFMV), transmitted by aphids.",
        "treatment": [
            "No chemical treatment available for viral infections.",
            "Rogue and destroy infected vines showing classic vein clearing or purplish rings."
        ],
        "prevention": [
            "Use certified virus-tested sweet potato vines for planting material.",
            "Control aphid populations and clear wild morning glory weeds near the plot."
        ]
    },
    "sweet_potato_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Maintain routine monitoring and ensure loose, well-aerated soil mounds."]
    },

    # =========================================================================
    # ADDITIONAL SYSTEM INFRASTRUCTURE / BACKUP MAPPINGS
    # =========================================================================
    "cashew_anthracnose": {
        "cause": "Fungus Colletotrichum gloeosporioides.",
        "treatment": ["Apply fungicides containing copper or mancozeb.", "Prune and destroy infected twigs and leaves."],
        "prevention": ["Plant resistant varieties.", "Ensure good air circulation.", "Avoid overhead irrigation."]
    },
    "cashew_gumosis": {
        "cause": "Fungus Lasiodiplodia theobromae.",
        "treatment": ["Surgical removal of infected bark and application of a fungicidal paste.", "Drenching the soil with fungicides."],
        "prevention": ["Avoid mechanical injuries to the tree.", "Maintain proper tree nutrition.", "Ensure good drainage."]
    },
    "cashew_healthy": {
        "cause": "N/A",
        "treatment": ["N/A"],
        "prevention": ["Maintain good agricultural practices."]
    },
    "cashew_leaf_miner": {
        "cause": "Insect pest Acrocercops syngramma.",
        "treatment": ["Apply systemic insecticides."],
        "prevention": ["Encourage natural predators."]
    },
    "cashew_red_rust": {
        "cause": "Alga Cephaleuros virescens.",
        "treatment": ["Apply copper-based fungicides."],
        "prevention": ["Improve air circulation and sunlight penetration."]
    },
    "soybean_rust": {
        "cause": "Fungus Phakopsora pachyrhizi.",
        "treatment": ["Fungicidal foliar applications containing triazoles or strobilurins upon first identification."],
        "prevention": ["Practice uniform rotation blocks using sorghum or maize crops.", "Plant early with initial rains."]
    },
    "sorghum_ergot": {
        "cause": "Fungus Claviceps africana.",
        "treatment": ["Clip and destroy infected panicles producing honey-dew fluid before hardening occurs."],
        "prevention": ["Incorporate deep autumn tilling regimes to bury soil sclerotia bodies.", "Use clean, certified seeds."]
    },
    "mosaic_virus": {
        "cause": "Various mosaic viruses affecting different plants.",
        "treatment": ["No cure. Remove and destroy infected plants."],
        "prevention": ["Use virus-free seeds/planting material.", "Control insect vectors (e.g., aphids)."]
    },
    "southern_blight": {
        "cause": "Fungus Sclerotium rolfsii.",
        "treatment": ["Apply fungicides.", "Deep plowing to bury sclerotia."],
        "prevention": ["Practice crop rotation with non-susceptible crops.", "Improve soil drainage."]
    },
    "sudden_death_syndrome": {
        "cause": "Fungus Fusarium virguliforme.",
        "treatment": ["No effective in-season treatment."],
        "prevention": ["Plant resistant varieties.", "Improve soil drainage and reduce compaction.", "Delay planting until soils are warmer."]
    }
}