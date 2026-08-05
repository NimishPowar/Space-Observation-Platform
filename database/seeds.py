"""Static seeders for normalized reference data and educational content.

These seeders populate database tables with initial reference material such as
planets, educational categories, and learning modules.
"""

from __future__ import annotations

from sqlalchemy.orm import Session

from database.models import EducationalCategory, EducationalContent, Planet


def seed_planets(session: Session) -> None:
    """Seed planetary reference records."""
    reference_planets = [
        {
            "name": "mars",
            "display_name": "Mars",
            "category": "terrestrial",
            "description": "The fourth planet from the Sun, known for its reddish appearance due to iron oxide on its surface.",
            "mass_kg": 6.39e23,
            "radius_km": 3389.5,
            "semi_major_axis_au": 1.52,
            "orbital_period_days": 687.0,
            "mean_density_g_cm3": 3.93,
            "source_url": "https://science.nasa.gov/mars/",
        },
        {
            "name": "jupiter",
            "display_name": "Jupiter",
            "category": "gas_giant",
            "description": "The largest planet in our solar system, famous for the Great Red Spot and its 4 Galilean moons.",
            "mass_kg": 1.898e27,
            "radius_km": 69911.0,
            "semi_major_axis_au": 5.20,
            "orbital_period_days": 4332.59,
            "mean_density_g_cm3": 1.33,
            "source_url": "https://science.nasa.gov/jupiter/",
        },
        {
            "name": "saturn",
            "display_name": "Saturn",
            "category": "gas_giant",
            "description": "Adorned with a dazzling, complex system of icy rings made of water ice, dust, and rock particles.",
            "mass_kg": 5.683e26,
            "radius_km": 58232.0,
            "semi_major_axis_au": 9.58,
            "orbital_period_days": 10759.22,
            "mean_density_g_cm3": 0.687,
            "source_url": "https://science.nasa.gov/saturn/",
        },
        {
            "name": "venus",
            "display_name": "Venus",
            "category": "terrestrial",
            "description": "The hottest planet in our solar system with a thick, toxic atmosphere of carbon dioxide and sulfuric acid clouds.",
            "mass_kg": 4.867e24,
            "radius_km": 6051.8,
            "semi_major_axis_au": 0.723,
            "orbital_period_days": 224.7,
            "mean_density_g_cm3": 5.243,
            "source_url": "https://science.nasa.gov/venus/",
        },
    ]

    for payload in reference_planets:
        existing = session.query(Planet).filter_by(name=payload["name"]).first()
        if existing is None:
            session.add(Planet(**payload))


def seed_educational_categories(session: Session) -> None:
    """Seed foundational educational taxonomy values."""
    categories = [
        {
            "slug": "solar-system",
            "name": "Solar System",
            "description": "Explore planets, dwarf planets, asteroids, comets, and major solar system bodies.",
        },
        {
            "slug": "lunar-phenomena",
            "name": "Lunar Phenomena",
            "description": "Understand Moon phases, tidal interactions, and surface features.",
        },
        {
            "slug": "eclipses",
            "name": "Eclipses & Alignments",
            "description": "Learn how solar and lunar eclipses occur through orbital geometry.",
        },
        {
            "slug": "stellar-astronomy",
            "name": "Stars & Nebulae",
            "description": "Discover stellar evolution, spectral classes, star clusters, and cosmic nebulae.",
        },
        {
            "slug": "deep-space",
            "name": "Deep Space & Cosmology",
            "description": "Examine galaxies, black holes, exoplanets, and cosmic structures across the universe.",
        },
    ]

    for payload in categories:
        existing = session.query(EducationalCategory).filter_by(slug=payload["slug"]).first()
        if existing is None:
            session.add(EducationalCategory(**payload))


def seed_educational_content(session: Session) -> None:
    """Seed comprehensive educational articles and guides."""
    cat_map = {c.slug: c.id for c in session.query(EducationalCategory).all()}

    articles = [
        {
            "category_id": cat_map.get("solar-system", 1),
            "title": "The Solar System",
            "slug": "solar-system",
            "excerpt": "A gravitationally bound system of the Sun and objects that orbit it, including 8 planets and dwarf planets.",
            "body": """
### Overview of the Solar System

Formed approximately 4.6 billion years ago from the gravitational collapse of a giant interstellar molecular cloud, our solar system contains one star (the Sun), eight major planets, dozens of dwarf planets, and millions of small bodies like asteroids and comets.

#### Structure
* **Inner Solar System**: Terrestrial rocky planets (Mercury, Venus, Earth, Mars).
* **Asteroid Belt**: Orbiting between Mars and Jupiter.
* **Outer Solar System**: Gas giants (Jupiter, Saturn) and Ice giants (Uranus, Neptune).
* **Kuiper Belt & Oort Cloud**: Cold realm of frozen icy bodies beyond Neptune.

#### Interesting Facts
* 99.86% of the solar system's total mass is concentrated in the Sun.
* Neptune takes 165 Earth years to complete a single orbit around the Sun.
* The Oort Cloud is believed to extend up to nearly a light-year from the Sun.
            """.strip(),
            "source_url": "https://science.nasa.gov/solar-system/",
            "is_featured": True,
        },
        {
            "category_id": cat_map.get("stellar-astronomy", 1),
            "title": "Stars and Stellar Evolution",
            "slug": "stars",
            "excerpt": "Luminous spheres of plasma held together by their own gravity, fueled by nuclear fusion in their cores.",
            "body": """
### Understanding Stars

Stars are the fundamental building blocks of galaxies. They produce heat, light, ultraviolet rays, x-rays, and other forms of radiation through nuclear fusion inside their cores.

#### Stellar Life Cycle
1. **Protostar**: Born in dense gas clouds inside nebulae.
2. **Main Sequence**: Stable core hydrogen fusion (e.g. our Sun).
3. **Red Giant / Supergiant**: Core hydrogen expands and turns to helium fusion.
4. **Stellar Remnant**: White dwarf, neutron star, or black hole depending on initial mass.

#### Interesting Facts
* The nearest star to Earth after the Sun is Proxima Centauri, 4.24 light-years away.
* Red dwarf stars are the most common stars in the universe and can burn for trillions of years.
* Neutron stars are so dense that a single teaspoon of neutron star material would weigh 6 billion tons on Earth.
            """.strip(),
            "source_url": "https://science.nasa.gov/universe/stars/",
            "is_featured": True,
        },
        {
            "category_id": cat_map.get("deep-space", 1),
            "title": "Galaxies: Cosmic Cities of Stars",
            "slug": "galaxies",
            "excerpt": "Massive gravitationally bound systems consisting of stars, stellar remnants, interstellar gas, and dark matter.",
            "body": """
### The Nature of Galaxies

Galaxies range in size from dwarfs with a few hundred million stars to giants with one hundred trillion stars.

#### Main Types of Galaxies
* **Spiral Galaxies**: Disk-like structures with spiral arms rich in gas and young stars (e.g. Milky Way, Andromeda).
* **Elliptical Galaxies**: Smooth, featureless, egg-shaped structures composed mostly of older stars.
* **Irregular Galaxies**: Chaotic shapes often resulting from gravitational interactions or collisions.

#### Interesting Facts
* There are estimated to be over 2 trillion galaxies in the observable universe.
* The Milky Way galaxy is expected to collide with the Andromeda galaxy in about 4.5 billion years.
* Most large galaxies harbor a supermassive black hole at their galactic core.
            """.strip(),
            "source_url": "https://science.nasa.gov/universe/galaxies/",
            "is_featured": True,
        },
        {
            "category_id": cat_map.get("stellar-astronomy", 1),
            "title": "Nebulae: Stellar Nurseries and Remnants",
            "slug": "nebulae",
            "excerpt": "Vast interstellar clouds of dust, hydrogen, helium, and ionized gases where new stars are born.",
            "body": """
### Cosmic Clouds

Nebulae are formed when cosmic dust and gas coalesce under gravity or when dying stars shed their outer envelopes into deep space.

#### Types of Nebulae
* **Emission Nebulae**: High-energy radiation illuminates ionized gas (e.g. Orion Nebula).
* **Reflection Nebulae**: Dust reflects light from nearby stars.
* **Planetary Nebulae**: Shells of gas ejected by dying low-mass stars like our Sun.
* **Supernova Remnants**: Expanding debris clouds from massive exploding stars (e.g. Crab Nebula).

#### Interesting Facts
* The Orion Nebula is the closest stellar nursery to Earth, located about 1,350 light-years away.
* Planetary nebulae have nothing to do with planets; early astronomers thought they looked like round gas giant planets through small telescopes.
            """.strip(),
            "source_url": "https://science.nasa.gov/missions/hubble/science/explore-the-night-sky/hubbles-messier-catalog/messier-42/",
            "is_featured": False,
        },
        {
            "category_id": cat_map.get("deep-space", 1),
            "title": "Black Holes: Gravity's Ultimate Triumph",
            "slug": "black-holes",
            "excerpt": "Regions of spacetime where gravity is so intense that nothing, not even light, can escape.",
            "body": """
### Extreme Physics of Black Holes

A black hole is formed when a massive star collapses under its own gravity at the end of its life, compressing mass into an infinitely dense point called a singularity.

#### Main Categories
* **Stellar Black Holes**: Formed by gravitational collapse of single massive stars (5-100 solar masses).
* **Supermassive Black Holes**: Millions to billions of solar masses residing at galactic centers (e.g. Sagittarius A*).

#### Key Concepts
* **Event Horizon**: The point of no return surrounding a black hole.
* **Spaghettification**: Extreme tidal forces stretching objects as they approach the event horizon.

#### Interesting Facts
* The first image of a black hole's shadow (M87*) was captured by the Event Horizon Telescope in 2019.
* Time slows down significantly near a black hole due to gravitational time dilation.
            """.strip(),
            "source_url": "https://science.nasa.gov/universe/black-holes/",
            "is_featured": True,
        },
        {
            "category_id": cat_map.get("deep-space", 1),
            "title": "Exoplanets: Worlds Beyond Our Solar System",
            "slug": "exoplanets",
            "excerpt": "Planets that orbit stars outside our solar system, offering clues to potential extraterrestrial habitability.",
            "body": """
### Discovering Alien Worlds

Thousands of exoplanets have been confirmed since the mid-1990s using space observatories like Kepler, TESS, and James Webb Space Telescope.

#### Detection Methods
* **Transit Method**: Measuring the subtle dimming of a star's brightness as a planet crosses in front of it.
* **Radial Velocity Method**: Detecting minute gravitational wobbles of a host star caused by an orbiting planet.

#### Planetary Types
* **Hot Jupiters**: Gas giants orbiting extremely close to their stars.
* **Super-Earths**: Planets larger than Earth but smaller than Neptune.
* **Habitable Zone Worlds**: Earth-sized planets receiving temperatures that allow liquid water on their surface.

#### Interesting Facts
* Over 5,500 exoplanets have been confirmed to date.
* The TRAPPIST-1 system contains seven Earth-sized terrestrial planets orbiting a cold red dwarf star.
            """.strip(),
            "source_url": "https://exoplanets.nasa.gov/",
            "is_featured": False,
        },
        {
            "category_id": cat_map.get("solar-system", 1),
            "title": "Comets: Icy Cosmic Snowballs",
            "slug": "comets",
            "excerpt": "Cosmic snowballs of frozen gas, rock, and dust that heat up and develop dramatic tails near the Sun.",
            "body": """
### Structure and Origin of Comets

Comets originate from the cold outer regions of the solar system—the Kuiper Belt and Oort Cloud.

#### Comet Anatomy
* **Nucleus**: Solid central core of ice and dust.
* **Coma**: Atmospheric cloud of gas surrounding the nucleus when heated by solar radiation.
* **Ion & Dust Tails**: Streaming gas and dust pushed away from the Sun by solar wind and photon pressure.

#### Interesting Facts
* Halley's Comet returns to the inner solar system every 75–76 years (next visit in 2061).
* Comet tails always point away from the Sun, regardless of the direction the comet is traveling.
            """.strip(),
            "source_url": "https://science.nasa.gov/solar-system/comets/",
            "is_featured": False,
        },
        {
            "category_id": cat_map.get("solar-system", 1),
            "title": "Asteroids: Rocky Remnants of Planet Formation",
            "slug": "asteroids",
            "excerpt": "Rocky, airless remnants left over from the early formation of our solar system 4.6 billion years ago.",
            "body": """
### Minor Planets

Most asteroids reside in the Main Asteroid Belt located between the orbits of Mars and Jupiter.

#### Classifications
* **Main Belt Asteroids**: Millions of rocky bodies orbiting between Mars and Jupiter.
* **Trojans**: Asteroids sharing an orbit with a larger planet (e.g. Jupiter Trojans).
* **Near-Earth Asteroids (NEAs)**: Asteroids whose orbits bring them close to Earth.

#### Interesting Facts
* Ceres is the largest object in the asteroid belt and is classified as both an asteroid and a dwarf planet.
* NASA's OSIRIS-REx mission successfully returned a sample from asteroid Bennu to Earth in 2023.
            """.strip(),
            "source_url": "https://science.nasa.gov/solar-system/asteroids/",
            "is_featured": False,
        },
        {
            "category_id": cat_map.get("lunar-phenomena", 1),
            "title": "Understanding Moon Phases",
            "slug": "moon-phases-guide",
            "excerpt": "A complete visual and physical guide to the 8 primary phases of the Moon as seen from Earth.",
            "body": """
### How Moon Phases Work

The Moon does not produce its own light; it reflects light from the Sun. As the Moon orbits Earth every 29.5 days (the synodic month), the fraction of its illuminated side visible from Earth changes continuously.

#### The 8 Primary Phases:
1. **New Moon**: The Moon is positioned between Earth and the Sun. The illuminated side faces away from Earth.
2. **Waxing Crescent**: A thin sliver of light appears on the right side (Northern Hemisphere) as the Moon moves eastward.
3. **First Quarter**: Half of the visible Moon disk is illuminated.
4. **Waxing Gibbous**: More than half of the visible disk is illuminated and growing.
5. **Full Moon**: Earth is between the Sun and Moon, revealing the fully lit hemisphere.
6. **Waning Gibbous**: The illuminated portion begins to shrink from right to left.
7. **Third Quarter**: The opposite half of the disk is illuminated.
8. **Waning Crescent**: A thin crescent visible in the early morning sky before sunrise.
            """.strip(),
            "source_url": "https://moon.nasa.gov/moon-in-motion/moon-phases/",
            "is_featured": True,
        },
        {
            "category_id": cat_map.get("eclipses", 1),
            "title": "Solar & Lunar Eclipses Explained",
            "slug": "eclipses-guide",
            "excerpt": "Discover how orbital inclination and syzygy create total, partial, and annular eclipses.",
            "body": """
### The Geometry of Eclipses

An eclipse happens when one astronomical object moves into the shadow of another body.

#### Solar Eclipses
Occur during a **New Moon** when the Moon passes directly between Earth and the Sun, casting its shadow (umbra and penumbra) onto Earth's surface.
* **Total Solar Eclipse**: The Moon completely covers the solar disk, revealing the solar corona.
* **Annular Solar Eclipse**: The Moon is near apogee (farthest point) and appears slightly smaller than the Sun, creating a 'ring of fire'.

#### Lunar Eclipses
Occur during a **Full Moon** when Earth passes directly between the Sun and Moon, casting Earth's shadow across the lunar surface.
* **Blood Moon**: During a total lunar eclipse, Earth's atmosphere scatters short blue light waves while refracting longer red wavelengths onto the Moon.
            """.strip(),
            "source_url": "https://science.nasa.gov/eclipses/",
            "is_featured": True,
        },
        {
            "category_id": cat_map.get("solar-system", 1),
            "title": "Mars: The Red Planet Overview",
            "slug": "mars-overview",
            "excerpt": "Explore the atmospheric conditions, surface dust storms, and orbital characteristics of Mars.",
            "body": """
### Mars Science Overview

Mars is the fourth planet from the Sun, orbiting at an average distance of 1.52 Astronomical Units (AU). It completes one orbit every 687 Earth days.

#### Key Features:
* **Atmosphere**: Thin, composed of 95% carbon dioxide, 2.6% nitrogen, and 1.9% argon.
* **Surface Geology**: Home to Olympus Mons (the tallest volcano in the solar system at 21.9 km) and Valles Marineris (a massive canyon system).
* **Observational Tip**: Best viewed during opposition, which occurs approximately every 26 months when Mars is closest to Earth.
            """.strip(),
            "source_url": "https://science.nasa.gov/mars/",
            "is_featured": False,
        },
        {
            "category_id": cat_map.get("solar-system", 1),
            "title": "Jupiter: King of the Planets",
            "slug": "jupiter-overview",
            "excerpt": "A deep dive into Jupiter's magnetosphere, Great Red Spot, and Galilean moons.",
            "body": """
### Jupiter Overview

Jupiter is a gas giant primarily composed of hydrogen and helium. Its intense gravitational influence helps shape the dynamics of the asteroid belt.

#### Galilean Moons:
1. **Io**: Most volcanically active body in the solar system.
2. **Europa**: Smooth icy crust concealing a global subsurface liquid ocean.
3. **Ganymede**: The largest moon in the solar system, even larger than Mercury.
4. **Callisto**: Heavily cratered, ancient icy surface.
            """.strip(),
            "source_url": "https://science.nasa.gov/jupiter/",
            "is_featured": True,
        },
    ]

    for payload in articles:
        existing = session.query(EducationalContent).filter_by(slug=payload["slug"]).first()
        if existing is None:
            session.add(EducationalContent(**payload))


def seed_reference_data(session: Session) -> None:
    """Run all static seeders into one session transaction."""
    seed_planets(session)
    seed_educational_categories(session)
    session.flush()
    seed_educational_content(session)
    session.commit()
