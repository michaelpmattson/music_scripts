from genres import *

genre_hierarchy = {
    alternative_rock: [rock],
    doom_metal: [heavy_metal],
    grunge: [alternative_rock],
    skate_punk: [punk],
    sludge_metal: [heavy_metal],
    punk: [rock],
    # Add more mappings as needed
}


def ensure_parent_genres(genres, hierarchy):
    expanded_genres = set(genres)

    def add_parents(genre):
        if genre in hierarchy:
            parents = hierarchy[genre]
            for parent in parents:
                if parent not in expanded_genres:
                    expanded_genres.add(parent)
                    add_parents(parent)

    for genre in genres:
        add_parents(genre)

    return sorted(expanded_genres)

# Example usage:
# genres = ['Skate punk', 'Crossover thrash']
# expanded_genres = ensure_parent_genres(genres, genre_hierarchy)
# print(expanded_genres)
