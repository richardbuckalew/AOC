def score(opp, me):
  shape_scores = {'X':1, 'Y':2, 'Z':3}
  win_shapes = [('A', 'Y'), ('B', 'Z'), ('C', 'X')]
  tie_shapes = [('A', 'X'), ('B', 'Y'), ('C', 'Z')]
  if (opp, me) in win_shapes:
    return 6 + shape_scores[me]
  elif (opp, me) in tie_shapes:
    return 3 + shape_scores[me]
  else:
    return shape_scores[me]

def get_myplay(opp, outcome):
  if outcome == 'Z': #win
    return {'A':'Y', 'B':'Z', 'C':'X'}[opp]
  elif outcome == 'Y': #tie
    return {'A':'X', 'B':'Y', 'C':'Z'}[opp]
  else:
    return {'A':'Z', 'B':'X', 'C':'Y'}[opp]

s = 0
for line in data.split('\n'):
  try:
    (opp, outcome) = line.split()
    me = get_myplay(opp, outcome)
    s += score(opp, me)
  except:
    pass

print(s)
