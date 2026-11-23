"""Generate 20 original, mathematically checked MCQs for every Grade 10 subtopic.
All explanations are deterministic. Tests reuse a different selection and do not reveal hints.
Run from the project root: python scripts/generate_questions.py
"""
import json, math, random, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
content=json.loads((ROOT/'data'/'curriculum.json').read_text(encoding='utf8'))
Q=[];TEST=[]

def fmt(x):
    if isinstance(x,str): return x
    if isinstance(x,int) or abs(x-round(x))<0.00000001:return str(round(x))
    return f'{x:.2f}'.rstrip('0').rstrip('.')

def mc(prompt, answer, alternatives, hint, reasoning):
    answer=str(answer)
    opts=[answer]+[str(x) for x in alternatives if str(x)!=answer]
    opts=list(dict.fromkeys(opts))
    for filler in ['Not enough information','None of these','All of these','0','1','−1']:
        if len(opts)>=4: break
        if filler not in opts:opts.append(filler)
    opts=opts[:4]
    assert len(opts)==4, (prompt,opts)
    rr=random.Random(int(hashlib.md5(prompt.encode('utf8')).hexdigest()[:8],16));rr.shuffle(opts)
    return dict(prompt=prompt,options=opts,answerIndex=opts.index(answer),hints=hint if isinstance(hint,list) else [hint,'Write down the relevant formula and substitute the known values.'],explanation=reasoning if isinstance(reasoning,list) else [reasoning],type='multiple-choice')

def num(prompt,answer,hint,reasoning,distractors=None):
    a=float(answer)
    if distractors is None:
        delta=max(1,round(abs(a)*0.22,2))
        distractors=[a+delta,a-delta,-a if a!=0 else a+2,a+2*delta,a-2*delta]
    used=[]
    for x in distractors:
        f=fmt(x)
        if f!=fmt(a) and f not in used: used.append(f)
    return mc(prompt,fmt(a),used,hint,reasoning)


# One contextual modeling question of each style per subtopic, both in practice
# and in the unseen checkpoint bank. They use age-appropriate everyday situations.
def applied(lid, i):
    k=i//2; m=i%2
    a=3+k; b=5+k
    if lid=='points-lines-planes':
        if not m:return num(f'On a hiking map, the trail starts at mile marker −{a} and ends at marker {b}. How long is the marked segment?',a+b,['Find the difference between the coordinate locations.','A distance cannot be negative.'],[f'{b}−(−{a})={a+b} miles.'])
        return num(f'Two delivery hubs are at street coordinates {2*a} and {2*b} km. Where is the midpoint pickup?',a+b,['Add the coordinates.','Divide by 2.'],[f'({2*a}+{2*b})/2={a+b} km.'])
    if lid=='angles-parallel':
        if not m:return num(f'A designer makes a straight wall joint of 180°. One angle is {a*3}°. What is the adjacent angle?',180-a*3,['A straight angle totals 180°.','Subtract the measured angle.'],[f'180−{a*3}={180-a*3}°.'])
        return num(f'Two parallel bike lanes are crossed by a diagonal path. A corresponding angle is {55+k}°. How large is its matching angle?',55+k,['Parallel lines preserve corresponding angle measures.','No subtraction is needed.'],[f'The matching angle measures {55+k}°.'])
    if lid=='logic-proofs':
        if not m:return mc(f'A blueprint for {a} frame sections says beam A has the same length as beam B, and beam B has the same length as beam C. What follows?', 'Beam A equals beam C',['Beam A is longer than C','Beam A is half of C','Nothing about A and C'],['This is a chain of equalities.','Use the transitive property.'],['A=B and B=C imply A=C by transitivity.'])
        return mc(f'In lab trial {a}, the rule is: IF a specimen exceeds the heat limit THEN its indicator turns red. The specimen exceeds the limit. What follows?', 'Its indicator turns red',['Its indicator stays blue','The limit was never reached','It must be frozen'],['Identify the hypothesis and conclusion.','This is an if-then statement with a true hypothesis.'],['By modus ponens, the stated consequence follows.'])
    if lid=='triangle-angles':
        if not m:return num(f'A triangular window has top angles {25+k}° and {45+k}°. What is the third interior angle?',110-2*k,['Interior angles of a triangle total 180°.','Subtract the two given measurements.'],[f'180−({25+k}+{45+k})={110-2*k}°.'])
        return num(f'A triangular roof frame has remote interior angles {30+k}° and {45+k}°. Find the exterior angle at the third corner.',75+2*k,['An exterior angle is the sum of the two remote interior angles.','Add the given angles.'],[f'{30+k}+{45+k}={75+2*k}°.'])
    if lid=='congruent-triangles':
        if not m:return mc(f'Two triangular glass panels each have sides {a}, {b}, and {a+b-1} cm. What theorem proves they are congruent?', 'SSS',['SAS','ASA','AAA'],['We know all three pairs of matching sides.','Choose the side-side-side theorem.'],['Matching all three sides proves SSS congruence.'])
        return mc(f'Two right-angle support brackets match in hypotenuse ({a+b} cm) and one leg ({a} cm). Which rule proves congruence?', 'HL',['AAA','SSA','AAS'],['Both triangles are right triangles.','Use the special hypotenuse-leg theorem.'],['Hypotenuse-leg (HL) proves right-triangle congruence.'])
    if lid=='triangle-inequality':
        if not m:return num(f'A carpenter has two braces of lengths {a} and {b}. What is the longest INTEGER third brace that could form a triangle?',a+b-1,['The longest side must be less than the sum of the other two.','Use strict inequality.'],[f'c<{a+b}; largest integer is {a+b-1}.'])
        return mc(f'A three-stick mobile uses lengths {a}, {b}, and {a+b+2}. Can these form a triangular frame?', 'No',['Yes','Only if the frame is equilateral','Only with a right angle'],['Compare the longest side with the sum of the shorter two.','The sum must be strictly greater.'],[f'{a}+{b}={a+b} is less than {a+b+2}; the triangle cannot close.'])
    if lid=='similar-triangles':
        if not m:return num(f'A model airplane wing is {a} cm long. The full-size wing is built at scale factor 4. How long is it in cm?',4*a,['New length = scale factor × old length.','Multiply by 4.'],[f'{a}×4={4*a} cm.'])
        return num(f'A square poster has area {b} cm². A scaled poster doubles each side. What is the new area in cm²?',4*b,['Area scales with the square of the side factor.','Doubling sides quadruples area.'],[f'{b}×2²={4*b} cm².'])
    if lid=='pythagorean-theorem':
        if not m:return num(f'A painter places a ladder {3*(k-7)} m from a wall and reaches {4*(k-7)} m up. How long is the ladder?',5*(k-7),['The ladder is the hypotenuse.','Use the Pythagorean theorem.'],[f'√({3*(k-7)}²+{4*(k-7)}²)={5*(k-7)} m.'])
        return num(f'A rectangular skate park is {a*3} m wide and {a*4} m long. What is its diagonal in meters?',a*5,['The diagonal forms a right triangle.','Apply the 3-4-5 ratio.'],[f'√({3*a}²+{4*a}²)={5*a} m.'])
    if lid=='right-triangle-trig':
        if not m:return mc(f'Looking up a {3*(k-7)} m tall sign from a point {4*(k-7)} m away forms a scaled 3–4–5 triangle. What is sin of the viewing angle?', '3/5',['4/5','3/4','5/3'],['Sine uses opposite over hypotenuse.','The sign height is opposite; the hypotenuse is 5.'],['sin θ=3/5.'])
        return mc(f'A ramp rises {5*(k-7)} m over {12*(k-7)} m of horizontal run. What is tan of its incline angle?', '5/12',['12/5','5/13','12/13'],['Tangent uses rise over horizontal run.','Use opposite/adjacent.'],['tan θ=5/12.'])
    if lid=='quadrilateral-properties':
        if not m:return num(f'An architect designs a {a}-sided courtyard. What is the sum of its interior angles, in degrees?',(a-2)*180,['Split the polygon into n−2 triangles.','Each triangle adds 180°.'],[f'({a}−2)×180={(a-2)*180}°.'])
        return num(f'A regular {b}-sided floor tile has equal interior angles. What is ONE interior angle, rounded to two decimals?',round((b-2)*180/b,2),['Find the total angle sum.','Divide by number of equal corners.'],[f'(({b}−2)×180)/{b}={fmt((b-2)*180/b)}°.'])
    if lid=='circle-angles':
        if not m:return num(f'A ferris-wheel viewpoint intercepts a {6*a}° arc. Find its inscribed angle measure.',3*a,['An inscribed angle is half the intercepted arc.','Divide by two.'],[f'{6*a}/2={3*a}°.'])
        return num(f'The rotating arm of a ride sweeps a {7*a}° arc about the center. What is the central angle?',7*a,['Central angle equals the arc measure.','The vertex lies at the center.'],[f'The central angle measures {7*a}°.'])
    if lid=='arcs-sectors':
        if not m:return mc(f'A sprinkler wets a quarter-circle arc of radius {a} m. What is the outer arc length in terms of π?',f'{fmt(a/2)}π',[f'{a}π',f'{2*a}π',f'{a*a}π'],['Quarter of circumference = (1/4)×2πr.','Keep π symbolic.'],[f'L=π×{a}/2={fmt(a/2)}π m.'])
        return mc(f'A pizza slice covers one quarter of a pizza of radius {b} cm. What is the slice area in terms of π?',f'{fmt(b*b/4)}π',[f'{b*b}π',f'{fmt(b*b/2)}π',f'{2*b}π'],['One quarter of the full circle area.','Area = πr²/4.'],[f'A={b}²π/4={fmt(b*b/4)}π cm².'])
    if lid=='area-perimeter':
        if not m:return num(f'A classroom rug is {a} m by {b} m. How many square meters does it cover?',a*b,['Area is length times width.','Area uses square units.'],[f'{a}×{b}={a*b} m².'])
        return num(f'A gardener fences a rectangular plot {a} m long and {b} m wide. How many meters of fencing are needed?',2*(a+b),['Fence runs around all four sides.','Perimeter=2(l+w).'],[f'2({a}+{b})={2*(a+b)} m.'])
    if lid=='surface-area':
        if not m:return num(f'A shipping box measures {a}×{b}×2 cm. How much cardboard surface area is needed for the CLOSED box?',2*(a*b+2*a+2*b),['Include every face.','SA=2(lw+lh+wh).'],[f'2({a*b}+{2*a}+{2*b})={2*(a*b+2*a+2*b)} cm².'])
        return mc(f'A closed soup can is radius 3 cm and height {a} cm. Find its surface area in terms of π.',f'{18+6*a}π',[f'{6*a}π','18π',f'{9*a}π'],['Add two bases and the curved surface.','SA=2πr²+2πrh.'],[f'2π(3²)+2π(3)({a})={18+6*a}π cm².'])
    if lid=='volume-solids':
        if not m:return num(f'A fish tank is {a} dm long, {b} dm wide and 2 dm deep. What is its volume in dm³?',2*a*b,['Multiply the three perpendicular dimensions.','Use cubic units.'],[f'{a}×{b}×2={2*a*b} dm³.'])
        return mc(f'A cylindrical rain barrel has radius 2 m and height {a} m. Find volume in terms of π.',f'{4*a}π',[f'{2*a}π',f'{8*a}π','4π'],['Cylinder volume=πr²h.','Square the radius.'],[f'V=π(2²)({a})={4*a}π m³.'])
    if lid=='function-notation':
        if not m:return num(f'A taxi charges ${a} pickup fee and ${b} per mile. If f(m)={a}+{b}m, find f(4).',a+4*b,['Substitute the miles into the function.','Include pickup fee once.'],[f'f(4)={a}+4×{b}={a+4*b} dollars.'])
        return num(f'A game awards score g(x)=x²+{a}x+{b}. How many points for x=3?',9+3*a+b,['Substitute 3 into both x terms.','Square first, multiply second.'],[f'g(3)=9+{3*a}+{b}={9+3*a+b}.'])
    if lid=='graph-transformations':
        if not m:return num(f'A ball path is modeled by y=−(x−{a})²+5. At which horizontal x is the peak?',a,['Vertex form gives the location of the peak.','x-coordinate is h.'],[f'The vertex is ({a},5), so the peak is at x={a}.'])
        return num(f'A parabola-based skate ramp is modeled by y=(x−2)²+{b}. What is its minimum height?',b,['The minimum y occurs at the vertex.','Read the outside shift k.'],[f'Minimum is y={b}.'])
    if lid=='function-composition':
        if not m:return num(f'A shop doubles a number then adds ${a} shipping. Starting from {b}, find f(g({b})) where g(x)=2x and f(x)=x+{a}.',2*b+a,['Apply g before f.','Double, then add shipping.'],[f'g({b})={2*b}; f({2*b})={2*b}+{a}={2*b+a}.'])
        return num(f'A game adds {a} bonus points then triples the score. For a starting score {b}, find g(f({b})) where f(x)=x+{a}, g(x)=3x.',3*(b+a),['Apply the bonus first, then the multiplier.','Composition order matters.'],[f'3({b}+{a})={3*(b+a)}.'])
    if lid=='factoring-quadratics':
        if not m:return mc(f'A model has height zero when x²+{a+b}x+{a*b}=0. Which values of x make the product zero?',f'−{a} and −{b}',[f'{a} and {b}',f'−{a+b} and −{a*b}',f'−{a} and {b}'],['Factor into two binomials.','Use the zero-product rule.'],[f'(x+{a})(x+{b})=0, so x=−{a}, −{b}.'])
        return num(f'An area model has sides (x+{a}) and (x+{b}). What is the CONSTANT term of its area polynomial?',a*b,['Multiply the two constant terms.','Expand (x+a)(x+b).'],[f'Constant term={a}×{b}={a*b}.'])
    if lid=='solving-quadratics':
        if not m:return num(f'A physics equation x²−{a+b}x+{a*b}=0 gives two crossing times. What is the earlier time x?',a,['Factor to find roots.','Take the smaller positive root.'],[f'(x−{a})(x−{b})=0; earlier x={a}.'])
        return num(f'An arch design uses x²−{a+b}x+{a*b}=0. Calculate its discriminant.',(b-a)**2,['D=b²−4ac.','Here roots differ by b−a.'],[f'D=({a+b})²−4({a*b})={(b-a)**2}.'])
    if lid=='complex-numbers':
        if not m:return mc(f'Two electrical phasors are {a}+2i and {b}+3i. What is their sum?',f'{a+b} + 5i',[f'{a+b} + 6i',f'{a*b} + 5i',f'{a+b+5}i'],['Add real components and imaginary components separately.','2i+3i=5i.'],[f'({a}+{b})+(2+3)i={a+b}+5i.'])
        power=4+a
        cycle=['1','i','−1','−i'];answer=cycle[power%4]
        return mc(f'In a rotation model, an operator uses i^{power}. What is its simplified value?',answer,[v for v in cycle if v!=answer],['Powers of i repeat in a four-step cycle.','Divide the exponent by 4 for the remainder.'],[f'i^{power}={answer}.'])
    if lid=='polynomial-operations':
        if not m:return num(f'A garden has dimensions (x+{a}) and (x+{b}). What is the coefficient of x in its expanded area formula?',a+b,['Expand the product.','The two cross terms combine.'],[f'Area=x²+{a+b}x+{a*b}; coefficient is {a+b}.'])
        return num(f'A panel uses (2x+{a})(3x+{b}) units of area. What is the constant term?',a*b,['Multiply the constant parts.','Only constant×constant yields a constant.'],[f'Constant term={a}×{b}={a*b}.'])
    if lid=='polynomial-division':
        if not m:return num(f'For a production polynomial P(x)=x²−{a}x+{b}, what remainder results when dividing by (x−2)?',4-2*a+b,['Apply the Remainder Theorem.','Substitute x=2.'],[f'P(2)=4−{2*a}+{b}={4-2*a+b}.'])
        return mc(f'A design polynomial factors as P(x)=(x−{a})(x+{b}). Is (x−{a}) a factor?', 'Yes',['No','Only when x=0','Not enough data'],['A factor appears explicitly in the product.','A zero at x=a confirms it.'],['Yes; P(a)=0.'])
    if lid=='polynomial-end-behavior':
        if not m:return mc(f'A long-term cost model has leading term −{a}x³. What does its graph do as positive x becomes extremely large?', 'Falls toward −∞',['Rises toward +∞','Approaches 0','Becomes periodic'],['The highest-degree term dominates.','A negative coefficient times positive x³ stays negative.'],['The right side falls toward negative infinity.'])
        return num(f'An experimental degree-{a} polynomial is graphed. What is the most turning points it could have?',a-1,['Degree n allows at most n−1 turning points.','Subtract one.'],[f'{a}−1={a-1}.'])
    if lid=='rational-expressions':
        if not m:return num(f'A simplified efficiency model is E(x)=(x²−{a*a})/(x−{a}) for x≠{a}. What is E({b+4})?',b+4+a,['Factor the difference of squares.','Cancel x−a only where x≠a.'],[f'E(x)=x+{a}, so E({b+4})={b+4+a}.'])
        return num(f'A machine rate model is R(x)=(x+2)/(x−{a}). At which input does this formula become undefined?',a,['Find the denominator zero.','Solve x−a=0.'],[f'x={a} is not allowed.'])
    if lid=='radical-equations':
        if not m:return num(f'A distance display shows √(x+{a})={b}. What value x generated the reading?',b*b-a,['Square both sides.','Subtract a and check the root.'],[f'x={b}²−{a}={b*b-a}.'])
        return num(f'A square tile has area {(a+1)**2} cm². What is its nonnegative side length?',a+1,['Side = positive square root of area.','Use principal square root.'],[f'√{(a+1)**2}={a+1} cm.'])
    if lid=='rational-asymptotes':
        if not m:return num(f'A rate model is R(x)=5/(x−{a})+2. Which x-value is its vertical asymptote?',a,['Denominator zero determines the vertical asymptote.','Solve x−a=0.'],[f'x={a}.'])
        return num(f'A temperature model is T(x)=4/(x−2)+{b}. As x grows very large, what does T approach?',b,['The reciprocal term shrinks toward 0.','Identify the remaining constant.'],[f'T(x)→{b}.'])
    if lid=='exponential-functions':
        if not m:return num(f'A class fund starts with ${100*(k+1)} and grows 10% annually. How much is in it after 2 years?',121*(k+1),['Use compound growth, not simple addition.','Multiply by 1.1 twice.'],[f'{100*(k+1)}×1.1²={121*(k+1)} dollars.'])
        return num(f'A phone battery model starts at {100+a} units and loses 20% each hour. How many units remain after two hours, rounded to 2 decimals?',round((100+a)*.8**2,2),['20% loss means retain 80% per period.','Multiply by 0.8 twice.'],[f'({100+a})×0.8²={fmt(round((100+a)*.64,2))}.'])
    if lid=='logarithms':
        if not m:return num(f'A computer repeatedly doubles data: 2^n={2**a}. What exponent n does log₂({2**a}) return?',a,['A logarithm reverses exponentiation.','Count doublings needed.'],[f'2^{a}={2**a}, hence n={a}.'])
        return num(f'A lab counts tripling steps using log₃(x)={a}. How many items are there after all steps?',3**a,['Rewrite in exponential form.','x=3^a.'],[f'x=3^{a}={3**a}.'])
    if lid=='arithmetic-geometric-sequences':
        if not m:return num(f'A student saves ${a} the first week and adds ${b} more each week than the last. How much is saved in WEEK 5?',a+4*b,['Arithmetic sequence: four increments from week 1 to week 5.','a₅=a₁+4d.'],[f'{a}+4×{b}={a+4*b} dollars.'])
        return num(f'A video is shared with {a} friends and the number reached triples each round. How many are reached in ROUND 4?',a*27,['Geometric sequence multiplies by 3 each round.','Round 4 is three jumps after round 1.'],[f'{a}×3³={a*27}.'])
    if lid=='center-spread':
        if not m:return num(f'Quiz scores are {a}, {a+2}, {a+4}, and {a+6}. Find the class mean.',a+3,['Add all four scores.','Divide by 4.'],[f'Mean={a+3}.'])
        return num(f'Two daily temperatures are {a-3}° and {a+3}°. Find their POPULATION standard deviation in degrees.',3,['Their mean is the midpoint.','Each observation lies 3 degrees from the mean.'],['σ=√((3²+3²)/2)=3°.'])
    if lid=='counting-principles':
        if not m:return num(f'A coach chooses two students from a pool of {a+2} for an unordered debate pair. How many possible pairs?',(a+2)*(a+1)//2,['Order is irrelevant.','Use nC2.'],[f'({a+2}×{a+1})/2={(a+2)*(a+1)//2}.'])
        return num(f'A club assigns president and vice president from {a+2} members. How many assignments are possible?',(a+2)*(a+1),['Different roles mean different orderings.','Use nP2.'],[f'({a+2})×({a+1})={(a+2)*(a+1)}.'])
    if lid=='conditional-probability':
        if not m:return num(f'Among {a+4} art-club students, {a} also take music. Given a student is in art club, what percent take music, rounded to 2 decimals?',round(a/(a+4)*100,2),['Condition on the art-club group only.','Divide overlap by this group total.'],[f'{a}/{a+4}×100={fmt(round(a/(a+4)*100,2))}%.'])
        return num(f'Of {b+5} school-bus riders, {b} carry a laptop. What is P(laptop | bus) as a percentage rounded to 2 decimals?',round(b/(b+5)*100,2),['Use bus riders as denominator.','Divide matching count by conditional population.'],[f'{b}/{b+5}×100={fmt(round(b/(b+5)*100,2))}%.'])
    if lid=='unit-circle':
        if not m:return mc(f'A robot arm rotates {90 if k<10 else 270}° counterclockwise. Convert this angle to radians.', 'π/2' if k<10 else '3π/2',['π/4','π','2π'],['A full rotation is 2π.','Convert degrees by multiplying π/180.'],[f'{90 if k<10 else 270}°={"π/2" if k<10 else "3π/2"} radians.'])
        return mc(f'A ferris wheel passenger is at angle {180 if k<10 else 360}° on the unit circle. What is the vertical coordinate sin θ?', '0',['1','−1','1/2'],['Sine is the y-coordinate.','Find the point on the unit circle.'],[f'sin({180 if k<10 else 360}°)=0.'])
    if lid=='law-sines':
        if not m:return num(f'A surveyor knows side a={a} m opposite a 30° angle. How long is side b opposite 90°?',2*a,['Match sides with opposite angles.','b=a×sin90/sin30.'],[f'b={a}×1/(1/2)={2*a} m.'])
        return num(f'A triangular sail has side a={2*a} cm opposite 90°. Find side b opposite 30°.',a,['Use the Law of Sines.','b=a×sin30/sin90.'],[f'b={2*a}×(1/2)/1={a} cm.'])
    if lid=='law-cosines':
        if not m:return num(f'Two hiking trails have lengths {a} and {b} km with a 60° included angle. Find the square of the straight-line distance c².',a*a+b*b-a*b,['Use c²=a²+b²−2ab cos60°.','cos60°=1/2.'],[f'c²={a*a}+{b*b}−{a*b}={a*a+b*b-a*b}.'])
        return num(f'Two perpendicular soccer-field edges are {a} and {b} m. By the Law of Cosines, find c² across their diagonal.',a*a+b*b,['The included angle is 90°.','cos90°=0.'],[f'c²={a*a}+{b*b}={a*a+b*b}.'])
    if lid=='domain-range':
        if not m:return num(f'A square-root distance model uses d(x)=√(x−{a}). What is the smallest possible input x?',a,['The radicand cannot be negative.','Solve x−a≥0.'],[f'x≥{a}.'])
        return num(f'A rate is R(x)=1/(x−{b}). What value x must a scientist EXCLUDE?',b,['The denominator must be nonzero.','Solve x−b=0.'],[f'x={b} is forbidden.'])
    if lid=='inverse-functions':
        if not m:return num(f'A converter uses f(x)=2x+{a}. If the output is {2*b+a}, what original input does f⁻¹ return?',b,['Undo addition, then division.','Inverse reverses the operation.'],[f'({2*b+a}−{a})/2={b}.'])
        return num(f'An encoding rule is f(x)=3x+{a}. Find y if the decoder f⁻¹(y) must output {b}.',3*b+a,['Apply f to both sides.','y=f(b).'],[f'y=3×{b}+{a}={3*b+a}.'])
    if lid=='transformations-modeling':
        if not m:return num(f'A study-room rental charges ${a} plus ${b} each hour. What is the 4-hour total?',a+4*b,['Use fixed + rate×time.','Remember the starting fee.'],[f'{a}+4×{b}={a+4*b} dollars.'])
        return num(f'A student sells 4 posters for ${b+6} each, spends ${a} per poster and pays a fixed $8 fee. What is profit?',4*(b+6-a)-8,['Profit = revenue−variable cost−fixed cost.','Calculate per-item margin first.'],[f'4({b+6}−{a})−8={4*(b+6-a)-8} dollars.'])
    return None

for lesson in content['lessons']:
    lid=lesson['id']; start=len(Q)
    for i in range(25):
        m=i%2;k=i//2;t=k+1
        q=None
        if lid=='points-lines-planes':
            a=-12+k; b=a+5+2*k
            if not m:q=num(f'On a number line, A={a} and B={b}. What is the length AB?',b-a,['Subtract the coordinates.','Take absolute value because a length is nonnegative.'],[f'AB = |{b} − ({a})| = {b-a}.'])
            else:q=num(f'What is the midpoint of the segment with endpoints {2*k-8} and {2*k+6}?',2*k-1,['Add the endpoints.','Divide their sum by 2.'],[f'Midpoint = ({2*k-8} + {2*k+6})/2 = {2*k-1}.'])
        elif lid=='angles-parallel':
            a=26+5*k
            if not m:q=num(f'An angle measures {a}°. What is its supplement?',180-a,['Supplementary angles total 180°.','Subtract the given angle from 180°.'],[f'180 − {a} = {180-a}°.'])
            else:q=num(f'Two parallel lines are cut by a transversal. One corresponding angle is {a+13}°. Find the other corresponding angle.',a+13,['Corresponding angles are congruent for parallel lines.','You do not need to subtract from 180°.'],[f'Corresponding angles match, so the angle is {a+13}°.'])
        elif lid=='logic-proofs':
            if not m:
                scenarios=[('A=B and B=C','A=C','Transitive property'),('AB=CD','CD=AB','Symmetric property'),('x=x','x=x','Reflexive property'),('If P then Q; P is true','Q is true','Modus ponens'),('A+B=B+A','A+B=B+A','Commutative property')]
                s,a,r=scenarios[k%5];q=mc(f'[{t}] Which conclusion follows from: {s}?',a,['A≠C','Nothing can be concluded','P is false', 'Q is false'],['Identify the logical statement already given.','Apply its matching rule; avoid assumptions from a diagram.'],[f'The {r.lower()} justifies {a}.'])
            else:
                scenarios=[('A=B and B=C','Transitive property'),('A=B so B=A','Symmetric property'),('AB=AB','Reflexive property'),('If P then Q and P, so Q','Modus ponens'),('x+y=y+x','Commutative property')]
                s,a=scenarios[k%5];q=mc(f'[{t}] Which reason justifies: {s}?',a,['Vertical angles theorem','Substitution only','Definition of midpoint','Distributive property'],['Identify whether equality is reversed, chained or repeated.','A valid proof reason must correspond to the exact statement.'],[f'{a} provides the required reasoning.'])
        elif lid=='triangle-angles':
            a=25+3*k; b=40+2*k
            if not m:q=num(f'A triangle has interior angles {a}° and {b}°. Find the third angle.',180-a-b,['Triangle interior angles sum to 180°.','Subtract both known measures.'],[f'180 − {a} − {b} = {180-a-b}°.'])
            else:q=num(f'Two remote interior angles of a triangle are {a}° and {b}°. Find the exterior angle.',a+b,['The exterior angle equals the sum of the remote interior angles.','Add the two angles.'],[f'{a} + {b} = {a+b}°.'])
        elif lid=='congruent-triangles':
            types=['SSS','SAS','ASA','AAS','HL']; a=types[k%5]
            if not m:
                descriptions={'SSS':'three pairs of matching sides','SAS':'two matching sides and the included angle','ASA':'two matching angles and the included side','AAS':'two matching angles and a non-included side','HL':'hypotenuse and a leg of two right triangles'}
                q=mc(f'Case {t}: Two triangles have {descriptions[a]}. Which congruence criterion applies?',a,[x for x in types if x!=a],['Underline the known parts.','Check whether the angle is INCLUDED between two sides.'],[f'These matching parts establish {a} congruence.'])
            else:
                bad=['AAA','SSA','Three angles','One side only','Two sides only'][k%5]
                q=mc(f'Case {t}: Which information is NOT sufficient by itself to prove triangle congruence?',bad,['SSS','SAS','ASA'],['List the accepted triangle congruence rules.','Angle-angle-angle only proves similarity; SSA is ambiguous.'],[f'{bad} is not a universally valid congruence criterion.'])
        elif lid=='triangle-inequality':
            a=3+k; b=7+k
            if not m:q=num(f'Two sides of a triangle are {a} and {b}. What is the greatest INTEGER length for the third side?',a+b-1,['The third side must be strictly LESS than the sum.','Use the largest integer below a+b.'],[f'c < {a+b}, so the greatest integer is {a+b-1}.'])
            else:
                c=a+b-1 if k%2==0 else a+b+1
                q=mc(f'Can segments of lengths {a}, {b} and {c} form a triangle?','Yes' if c<a+b else 'No',['No' if c<a+b else 'Yes','Only if right-angled','Only if isosceles'],['Add the two shorter lengths.','Their sum must be greater than the longest side.'],[f'{a}+{b}={a+b}, compared to {c}; the triangle inequality '+('holds.' if c<a+b else 'fails.')])
        elif lid=='similar-triangles':
            side=3+k; factor=2+k%3
            if not m:q=num(f'A side of length {side} is enlarged with scale factor {factor}. What is its new length?',side*factor,['Corresponding lengths multiply by the scale factor.','New = original × factor.'],[f'{side} × {factor} = {side*factor}.'])
            else:q=num(f'A shape of area {4+k} is enlarged with scale factor {factor}. What is the new area?',(4+k)*factor**2,['Area scales by the SQUARE of the length scale factor.','Multiply the original area by k².'],[f'Area = {4+k} × {factor}² = {(4+k)*factor**2}.'])
        elif lid=='pythagorean-theorem':
            triples=[(3,4,5),(5,12,13),(8,15,17),(7,24,25),(9,40,41)]
            a,b,c=triples[k%5];scale=1+k//5
            if not m:q=num(f'A right triangle has legs {a*scale} and {b*scale}. Find the hypotenuse.',c*scale,['Use a²+b²=c².','Take the positive square root.'],[f'c = √({a*scale}² + {b*scale}²) = {c*scale}.'])
            else:q=num(f'A right triangle has hypotenuse {c*scale} and one leg {a*scale}. Find the other leg.',b*scale,['Rearrange to b²=c²−a².','Take the positive square root.'],[f'b = √({c*scale}² − {a*scale}²) = {b*scale}.'])
        elif lid=='right-triangle-trig':
            a,b,c=[(3,4,5),(5,12,13),(8,15,17),(7,24,25),(9,40,41)][k%5]
            scale=1+k//5; a*=scale; b*=scale; c*=scale
            if not m:q=mc(f'In a right triangle, opposite={a}, adjacent={b}, hypotenuse={c}. What is sin θ?',f'{a}/{c}',[f'{b}/{c}',f'{a}/{b}',f'{c}/{a}'],['SOH: sine = opposite / hypotenuse.','The hypotenuse is the longest side.'],[f'sin θ = {a}/{c}.'])
            else:q=mc(f'In a right triangle, opposite={a}, adjacent={b}, hypotenuse={c}. What is tan θ?',f'{a}/{b}',[f'{b}/{a}',f'{a}/{c}',f'{b}/{c}'],['TOA: tangent = opposite / adjacent.','Do not use the hypotenuse in tangent.'],[f'tan θ = {a}/{b}.'])
        elif lid=='quadrilateral-properties':
            n=4+k
            if not m:q=num(f'Find the sum of interior angles of a {n}-sided polygon, in degrees.',(n-2)*180,['Divide the polygon into n−2 triangles.','Each triangle has 180°.'],[f'({n}−2)×180 = {(n-2)*180}°.'])
            else:q=num(f'A regular {n}-sided polygon has equal interior angles. What is ONE interior angle in degrees?',(n-2)*180/n,['Find total interior angle sum.','Divide by the number of sides.'],[f'(({n}−2)×180)/{n} = {fmt((n-2)*180/n)}°.'])
        elif lid=='circle-angles':
            arc=40+10*k
            if not m:q=num(f'An inscribed angle intercepts an arc of {arc}°. Find the angle measure.',arc/2,['An inscribed angle measures half its intercepted arc.','Divide the arc measure by 2.'],[f'{arc}/2 = {fmt(arc/2)}°.'])
            else:q=num(f'A central angle intercepts an arc of {arc}°. Find the central angle.',arc,['Central angle equals intercepted arc measure.','No halving is needed here.'],[f'The angle is {arc}°.'])
        elif lid=='arcs-sectors':
            r=3+k;theta=90 if k%2==0 else 180
            if not m:
                val=round(theta/360*2*r,4)
                q=mc(f'A circle has radius {r} and a central angle {theta}°. Find the arc length in terms of π.',f'{fmt(val)}π',[f'{fmt(val*2)}π',f'{fmt(r*2)}π',f'{fmt(r*r)}π'],['Arc length = (θ/360)×2πr.','Keep π symbolic.'],[f'({theta}/360)×2×{r}π = {fmt(val)}π.'])
            else:
                val=round(theta/360*r*r,4)
                q=mc(f'A circle has radius {r} and a sector angle {theta}°. Find the sector AREA in terms of π.',f'{fmt(val)}π',[f'{fmt(val*2)}π',f'{fmt(r*r)}π',f'{fmt(r*2)}π'],['Sector area = (θ/360)×πr².','The radius is squared for area.'],[f'({theta}/360)×{r}²π = {fmt(val)}π.'])
        elif lid=='area-perimeter':
            l=5+k;w=3+k
            if not m:q=num(f'A rectangle measures {l} by {w}. What is its area?',l*w,['Area = length × width.','Use square units.'],[f'{l}×{w}={l*w} square units.'])
            else:q=num(f'A rectangle measures {l} by {w}. What is its perimeter?',2*(l+w),['Perimeter is the distance around the edges.','Add l+w+l+w.'],[f'2({l}+{w})={2*(l+w)} units.'])
        elif lid=='surface-area':
            l=2+k;w=3+k;h=4+k
            if not m:q=num(f'A rectangular prism is {l}×{w}×{h}. Find its total surface area.',2*(l*w+l*h+w*h),['There are three pairs of equal faces.','SA=2(lw+lh+wh).'],[f'2({l*w}+{l*h}+{w*h})={2*(l*w+l*h+w*h)} square units.'])
            else:
                r=2+k;hh=3+k;v=2*r*r+2*r*hh
                q=mc(f'A closed cylinder has radius {r} and height {hh}. Find total surface area in terms of π.',f'{v}π',[f'{r*r*2}π',f'{2*r*hh}π',f'{v+r}π'],['Count two circular bases and one lateral wrap.','SA=2πr²+2πrh.'],[f'2({r}²)π+2({r})({hh})π={v}π.'])
        elif lid=='volume-solids':
            l=2+k;w=3+k;h=4+k
            if not m:q=num(f'A rectangular prism is {l}×{w}×{h}. Find its volume.',l*w*h,['Volume = length × width × height.','Use cubic units.'],[f'{l}×{w}×{h}={l*w*h} cubic units.'])
            else:
                r=2+k;h=3+k;v=r*r*h
                q=mc(f'A cylinder has radius {r} and height {h}. Find its volume in terms of π.',f'{v}π',[f'{r*h}π',f'{2*r*h}π',f'{r*r}π'],['V=πr²h.','Square the radius, then multiply by height.'],[f'{r}²×{h}π={v}π cubic units.'])
        elif lid=='function-notation':
            a=2+k;b=3+k;x=k-2
            if not m:q=num(f'If f(x)={a}x+{b}, what is f({x})?',a*x+b,['Replace x with the input.','Multiply before adding.'],[f'f({x})={a}({x})+{b}={a*x+b}.'])
            else:q=num(f'If g(x)=x²+{a}x+{b}, what is g({x})?',x*x+a*x+b,['Substitute into every x.','Apply the exponent before multiplication.'],[f'g({x})={x}²+{a}({x})+{b}={x*x+a*x+b}.'])
        elif lid=='graph-transformations':
            h=2+k;v=k-4
            if not m:q=num(f'Find the x-coordinate of the vertex of y=(x−{h})²+{v}.',h,['Compare with y=(x−h)²+k.','Inside (x−h) means vertex x=h.'],[f'The vertex is ({h}, {v}), so x={h}.'])
            else:q=num(f'Find the y-coordinate of the vertex of y=2(x−{h})²+{v}.',v,['The added constant outside gives the vertical shift.','Vertex y=k.'],[f'The vertex is ({h}, {v}), so y={v}.'])
        elif lid=='function-composition':
            a=2+k;b=1+k;x=k%4+1
            if not m:q=num(f'Let f(x)={a}x+{b}, g(x)=x². Find f(g({x})).',a*x*x+b,['Apply g first.','Now substitute the result into f.'],[f'g({x})={x*x}; f({x*x})={a}×{x*x}+{b}={a*x*x+b}.'])
            else:q=num(f'Let f(x)=x+{a}, g(x)=2x−{b}. Find g(f({x})).',2*(x+a)-b,['The inner function is f.','Apply g to the value f(x).'],[f'f({x})={x+a}; g({x+a})=2({x+a})−{b}={2*(x+a)-b}.'])
        elif lid=='factoring-quadratics':
            a=2+k;b=3+k
            if not m:
                ans=f'−{a} and −{b}'
                q=mc(f'Solve x²+{a+b}x+{a*b}=0. Which are the roots?',ans,[f'{a} and {b}',f'−{a+b} and −{a*b}',f'−{a} and {b}'],['Find two numbers adding to the x coefficient.','Factor to (x+a)(x+b)=0.'],[f'(x+{a})(x+{b})=0, so x=−{a} or x=−{b}.'])
            else:q=num(f'What constant c makes x²+{a+b}x+c factor as (x+{a})(x+{b})?',a*b,['Multiply the constant terms.','The constant is a×b.'],[f'{a}×{b}={a*b}.'])
        elif lid=='solving-quadratics':
            r1=k+1;r2=r1+2+(k%3);b=-(r1+r2);c=r1*r2
            if not m:q=num(f'Find the discriminant of x²{b:+d}x+{c}=0.',b*b-4*c,['D=b²−4ac.','Here a=1; carefully square the negative b.'],[f'D=({b})²−4×1×{c}={b*b-4*c}.'])
            else:q=num(f'Find the SMALLER root of x²{b:+d}x+{c}=0.',r1,['Factor as (x−r₁)(x−r₂).','Or apply the quadratic formula.'],[f'The equation factors as (x−{r1})(x−{r2})=0; smaller root = {r1}.'])
        elif lid=='complex-numbers':
            a=2+k;b=3+k;c=k-4;d=-2-k
            if not m:
                ans=f'{a+c} {"+" if b+d>=0 else "−"} {abs(b+d)}i'
                opts=[f'{a-c} + {abs(b-d)}i',f'{a+c} + {b-d}i',f'{a*c} + {b*d}i']
                q=mc(f'Simplify ({a}+{b}i)+({c}{d:+d}i).',ans,opts,['Combine real parts separately from i terms.','Add the coefficients of i.'],[f'Real: {a}+({c})={a+c}. Imaginary: {b}+({d})={b+d}. Result = {ans}.'])
            else:
                power=10+k; cycle=['1','i','−1','−i'];ans=cycle[power%4]
                q=mc(f'What is i^{power}?',ans,[v for v in cycle if v!=ans],['Powers of i repeat every four.','Find the remainder when dividing the exponent by 4.'],[f'{power} mod 4 = {power%4}; i^{power}={ans}.'])
        elif lid=='polynomial-operations':
            a=2+k;b=3+k
            if not m:q=num(f'What is the coefficient of x in (x+{a})(x+{b})?',a+b,['Distribute both binomials.','The middle terms are ax and bx.'],[f'x²+({a}+{b})x+{a*b}; coefficient={a+b}.'])
            else:q=num(f'What is the constant term in (2x+{a})(3x+{b})?',a*b,['Only multiply the constants to get the constant term.','Other products contain x.'],[f'Constant = {a}×{b}={a*b}.'])
        elif lid=='polynomial-division':
            c=k+1;a=k+2+(k%4);b=k+3+(k%5)
            if not m:
                val=c*c-a*c+b
                q=num(f'Find remainder when P(x)=x²−{a}x+{b} is divided by (x−{c}).',val,['Remainder theorem: remainder=P(c).','Substitute c into the polynomial.'],[f'P({c})={c}²−{a}({c})+{b}={val}.'])
            else:
                p=c+2
                q=mc(f'Is (x−{c}) a factor of P(x)=x²−{c+p}x+{c*p}?','Yes',['No','Only if x=0','Not enough information'],['A factor makes the remainder zero.','Substitute x=c into P(x).'],[f'P({c})={c*c}−{c+p}×{c}+{c*p}=0; yes, it is a factor.'])
        elif lid=='polynomial-end-behavior':
            n=2+k;a=-(k+1) if k%2 else k+1
            if not m:q=mc(f'For f(x)={a}x^{n}+lower-degree terms, what happens as x→+∞?','f(x)→+∞' if a>0 else 'f(x)→−∞',['f(x)→−∞' if a>0 else 'f(x)→+∞','f(x)→0','f(x) oscillates'],['The leading term controls end behavior.','Positive large x raised to any positive degree stays positive.'],[f'Leading coefficient is {"positive" if a>0 else "negative"}, so the right end points {"up" if a>0 else "down"}.'])
            else:q=num(f'What is the MAXIMUM possible number of turning points for a degree-{n+1} polynomial?',n,['At most n−1 turns for degree n.','Subtract 1 from the polynomial degree.'],[f'Degree {n+1} allows at most {n} turning points.'])
        elif lid=='rational-expressions':
            a=2+k;b=4+k;x=10+k
            if not m:q=num(f'For x≠{a}, simplify (x²+{b-a}x−{a*b})/(x−{a}) then evaluate at x={x}.',x+b,['Factor the numerator as (x−a)(x+b).','Cancel the shared factor, then substitute x.'],[f'(x−{a})(x+{b})/(x−{a})=x+{b}, so at {x} it is {x+b}.'])
            else:q=num(f'For expression (x+{b})/(x−{a}), which x-value is EXCLUDED from the domain?',a,['The denominator must not be zero.','Solve x−a=0.'],[f'x−{a}=0 at x={a}; that input is excluded.'])
        elif lid=='radical-equations':
            a=2+k;c=3+k;v=a*a-c
            if not m:q=num(f'Solve √(x+{c})={a}. Find x.',v,['Square BOTH sides after isolating the radical.','Then subtract the constant.'],[f'x+{c}={a*a}, so x={v}; check √{a*a}={a}.'])
            else:q=num(f'Simplify √{(a+2)**2}.',a+2,['The principal square root is nonnegative.','√(n²)=|n|.'],[f'√{(a+2)**2}={a+2}.'])
        elif lid=='rational-asymptotes':
            h=2+k;v=k-3;a=3+k
            if not m:q=num(f'For f(x)={a}/(x−{h})+({v}), find the vertical asymptote x=?.',h,['Set the denominator to zero.','A vertical shift does not change x=h.'],[f'x−{h}=0, giving x={h}.'])
            else:q=num(f'For f(x)={a}/(x−{h})+({v}), find the horizontal asymptote y=?.',v,['As x grows, the reciprocal fraction approaches 0.','What constant remains?'],[f'{a}/(x−{h})→0; thus y={v}.'])
        elif lid=='exponential-functions':
            initial=100*(k+1);rate=10+k
            if not m:
                val=initial*(1+rate/100)**2
                q=num(f'An amount of {initial} grows {rate}% per year. What is its value after 2 years? Round to 2 decimals.',round(val,2),['Use growth factor 1+r.','Compute A=A₀(1+r)².'],[f'{initial}×(1+{rate}/100)²={fmt(round(val,2))}.'])
            else:
                val=initial*(1-rate/100)**2
                q=num(f'An amount of {initial} DECREASES {rate}% per year. What is its value after 2 years? Round to 2 decimals.',round(val,2),['For decay use 1−r.','The percentage applies to the remaining amount each year.'],[f'{initial}×(1−{rate}/100)²={fmt(round(val,2))}.'])
        elif lid=='logarithms':
            b=2+(k%3);p=2+k
            if not m:q=num(f'Evaluate log_{b}({b**p}).',p,['A logarithm asks for an exponent.','What power of the base gives the argument?'],[f'{b}^{p}={b**p}; log_{b}({b**p})={p}.'])
            else:q=num(f'Solve log_{b}(x)={p}. Find x.',b**p,['Rewrite in exponential form.','x=base raised to the given logarithm.'],[f'x={b}^{p}={b**p}.'])
        elif lid=='arithmetic-geometric-sequences':
            first=3+k;d=2+k%4;n=5+k%4;r=2+k%2
            if not m:q=num(f'An arithmetic sequence starts at {first} with common difference {d}. Find term {n}.',first+(n-1)*d,['Use aₙ=a₁+(n−1)d.','There are n−1 steps from the first term.'],[f'{first}+({n}−1)×{d}={first+(n-1)*d}.'])
            else:q=num(f'A geometric sequence starts at {first} with common ratio {r}. Find term {n}.',first*r**(n-1),['Use aₙ=a₁r^(n−1).','Multiplication repeats n−1 times.'],[f'{first}×{r}^{n-1}={first*r**(n-1)}.'])
        elif lid=='center-spread':
            a=2+k;d=1+k%4
            if not m:q=num(f'Find the mean of data: {a}, {a+2}, {a+4}, {a+6}.',a+3,['Add the four values.','Divide by the count 4.'],[f'Mean = ({a}+{a+2}+{a+4}+{a+6})/4={a+3}.'])
            else:q=num(f'Find the POPULATION standard deviation of the two values {a-d} and {a+d}.',d,['The mean is the midpoint of the values.','Each value is d away; the population standard deviation is d.'],[f'Mean={a}; deviations are ±{d}; σ=√(({d}²+{d}²)/2)={d}.'])
        elif lid=='counting-principles':
            n=5+k
            if not m:q=num(f'From {n} students, how many UNORDERED pairs can be chosen?',n*(n-1)//2,['Order does not matter: use combinations.','nC2=n(n−1)/2.'],[f'{n}C2={n}×{n-1}/2={n*(n-1)//2}.'])
            else:q=num(f'From {n} students, how many ways can you assign a president and vice president?',n*(n-1),['Different roles mean order matters.','Use nP2=n(n−1).'],[f'{n}P2={n}×{n-1}={n*(n-1)}.'])
        elif lid=='conditional-probability':
            total=5+k;both=2+k%3
            if not m:q=num(f'Among {total} students in robotics, {both} also play tennis. What is P(tennis | robotics) as a PERCENT rounded to 2 decimals?',round(both/total*100,2),['Restrict the sample space to robotics students.','Divide overlap by robotics total and multiply by 100.'],[f'{both}/{total}×100={fmt(round(both/total*100,2))}%.'])
            else:
                denom=total+5; fav=2+k%3
                q=num(f'Of {denom} students who ride the bus, {fav} wear glasses. Find P(glasses | bus) as a PERCENT rounded to 2 decimals.',round(fav/denom*100,2),['The condition tells you the denominator.','Divide the matching group by the group satisfying the condition.'],[f'{fav}/{denom}×100={fmt(round(fav/denom*100,2))}%.'])
        elif lid=='unit-circle':
            vals=[(30,'π/6'),(45,'π/4'),(60,'π/3'),(90,'π/2'),(120,'2π/3'),(135,'3π/4'),(150,'5π/6'),(180,'π'),(270,'3π/2'),(360,'2π'),(390,'13π/6'),(405,'9π/4'),(420,'7π/3')]
            deg,rad=vals[k]
            if not m:q=mc(f'Convert {deg}° to radians.',rad,['π/2','π/3','π/4','2π','3π/2','5π/6'],['Multiply degrees by π/180.','Reduce the fraction.'],[f'{deg}×π/180={rad}.'])
            else:
                sin=['1/2','√2/2','√3/2','1','√3/2','√2/2','1/2','0','−1','0','1/2','√2/2','√3/2'][k]
                q=mc(f'What is sin({deg}°) on the unit circle?',sin,['0','1/2','√2/2','√3/2','1','−1/2','−√2/2','−√3/2'],['Sine equals the y-coordinate on the unit circle.','Use the reference angle and quadrant sign.'],[f'The unit-circle y-coordinate at {deg}° is {sin}.'])
        elif lid=='law-sines':
            a=4+k
            if not m:q=num(f'In a triangle, side a={a} is opposite A=30°. Find b opposite B=90°.',2*a,['Use a/sinA=b/sinB.','sin30°=1/2, sin90°=1.'],[f'b={a}×sin90°/sin30°={a}×2={2*a}.'])
            else:q=num(f'In a triangle, side a={2*a} is opposite A=90°. Find b opposite B=30°.',a,['Pair each side with its OPPOSITE angle.','b=a×sin30°/sin90°.'],[f'b={2*a}×(1/2)/1={a}.'])
        elif lid=='law-cosines':
            a=3+k;b=5+k
            if not m:
                val=a*a+b*b-a*b
                q=num(f'Two sides of a triangle have lengths {a} and {b} with included angle 60°. What is c² by the Law of Cosines?',val,['c²=a²+b²−2ab cos C.','cos60°=1/2, so subtract ab.'],[f'c²={a}²+{b}²−{a}×{b}={val}.'])
            else:
                val=a*a+b*b
                q=num(f'Two sides are {a} and {b} with included angle 90°. What is c² using the Law of Cosines?',val,['At 90°, cos C=0.','The Law of Cosines becomes the Pythagorean theorem.'],[f'c²={a}²+{b}²−0={val}.'])
        elif lid=='domain-range':
            a=2+k
            if not m:q=num(f'For f(x)=√(x−{a}), what is the SMALLEST allowed real x?',a,['The square-root input must be ≥0.','Solve x−a≥0.'],[f'x−{a}≥0 implies x≥{a}.'])
            else:q=num(f'For g(x)=1/(x−{a}), which real x is EXCLUDED from the domain?',a,['Denominators cannot be zero.','Solve x−a=0.'],[f'x={a} makes the denominator zero.'])
        elif lid=='inverse-functions':
            a=2+k;b=3+k;x=2+k%3;y=a*x+b
            if not m:q=num(f'f(x)={a}x+{b}. Evaluate f⁻¹({y}).',x,['An inverse undoes f.','Solve (y−b)/a.'],[f'f({x})={y}, so f⁻¹({y})={x}.'])
            else:
                v=3+k;result=(a*v)+b
                q=num(f'For f(x)={a}x+{b}, what value y satisfies f⁻¹(y)={v}?',result,['Apply f to both sides.','If f⁻¹(y)=v, then y=f(v).'],[f'y=f({v})={a}×{v}+{b}={result}.'])
        elif lid=='transformations-modeling':
            fixed=5+k;rate=3+k;h=2+k
            if not m:q=num(f'A rental charges ${fixed} fixed plus ${rate} per hour. Find total after {h} hours.',fixed+rate*h,['Cost = fixed charge + hourly charge×hours.','Include the fixed amount once.'],[f'{fixed}+{rate}×{h}={fixed+rate*h} dollars.'])
            else:
                price=15+k;variable=5+k%4;fixed=12+k;qnty=3+k
                val=(price-variable)*qnty-fixed
                q=num(f'A seller earns ${price} per item and pays ${variable} per item plus ${fixed} fixed cost. Find profit on {qnty} items.',val,['Profit = revenue − total costs.','Per-item margin times units, minus fixed cost.'],[f'({price}−{variable})×{qnty}−{fixed}={val} dollars.'])
        else:
            raise ValueError('Missing generator for '+lid)
        if i in (18,19,22,23): q=applied(lid,i) or q
        q.update(id=f'{lid}-{i+1:02d}' if i<20 else f'{lid}-checkpoint-{i-19:02d}',lessonId=lid,difficulty=['Fundamentals','Apply','Challenge'][i%3],skill=lesson['title'])
        if i<20: Q.append(q)
        else: TEST.append(q)
    assert len(Q)-start==20,lid

# Validate uniqueness and each answer is in the options.
from collections import Counter
counts=Counter(q['lessonId'] for q in Q)
assert len(Q)==780 and len(TEST)==195 and len(counts)==39 and all(x==20 for x in counts.values())
for lid in counts:
    prompts=[q['prompt'] for q in Q if q['lessonId']==lid]
    assert len(prompts)==len(set(prompts)),f'duplicate prompt in {lid}'
for q in Q+TEST:
    assert len(q['options'])==4 and 0<=q['answerIndex']<4 and len(set(q['options']))==4,q
    assert all(q['hints']) and all(q['explanation'])
(ROOT/'data'/'question-bank.json').write_text(json.dumps(Q,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'data'/'checkpoint-bank.json').write_text(json.dumps(TEST,ensure_ascii=False,indent=2),encoding='utf8')
print('Generated',len(Q),'practice questions and',len(TEST),'independent checkpoint items')
