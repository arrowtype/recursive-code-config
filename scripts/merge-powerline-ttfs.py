"""
    Script to include PowerLine glyphs by merging powerline-only TTFs with Rec Mono TTFs.
    More background at https://github.com/arrowtype/recursive/issues/351

    Work in progress.
    - Current blocker: PUA unicodes for glyphs like the "branch" arrow are getting dropped.
"""


from fontTools.merge import Merger

files = [
    "./fonts/RecMonoCasual/RecMonoCasual-Regular-1.064.ttf",
    "./font-data/NerdfontsPL-Regular Casual.ttf"
]

outputPath = "./fonts/RecMonoCasual/RecMonoCasual-PL.ttf"

merged = Merger().merge(files)

merged.save(outputPath)
