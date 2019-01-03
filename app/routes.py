from flask import render_template, url_for, redirect, request, session
from app import app
from app.models import Word
from app.forms import InputWords
from app.helper_utils import get_semantic_neighbor_graphemes, get_portmanteaus, get_rhymes
from app.global_constants import MAX_PORTMANTEAUS, MAX_RHYMES
import pdb

def get_puns_from_form_data(form):
    # Find the semantic neighbors of the graphemes
    nearest_graphemes1 = get_semantic_neighbor_graphemes(form.word1.data)
    nearest_graphemes2 = get_semantic_neighbor_graphemes(form.word2.data)

    # Find the Word objects corresponding to each of the semantic neighbors
    nearest_words1 = Word.query.filter(Word.grapheme.in_(nearest_graphemes1)).all()
    nearest_words2 = Word.query.filter(Word.grapheme.in_(nearest_graphemes2)).all()

    # Generate the ordered portmanteaus and rhymes
    portmanteaus = get_portmanteaus(nearest_words1, nearest_words2)
    rhymes = get_rhymes(nearest_words1, nearest_words2)

    return {'portmanteaus': map(lambda x: x.__str__(), portmanteaus[:MAX_PORTMANTEAUS]), 'rhymes': map(lambda x: x.__str__(), rhymes[:MAX_RHYMES])}

@app.route('/')
@app.route('/generate_puns', methods=['GET', 'POST'])
def generate_puns():
    '''
    Display the results, and continue prompting for input
    '''
    form = InputWords()
    if form.validate_on_submit():
        # This may crash if invalid inputs are provided... we'll see
        session['results'] = get_puns_from_form_data(form)
        # Pass the results on to 'results'
        return redirect(url_for('results'))
    return render_template('generate_puns.html', form=form)

@app.route('/results', methods=['GET', 'POST'])
def results():
    '''
    Display the results, and continue prompting for input
    '''
    # Pass the results on to
    return render_template('results.html', results=session['results'])