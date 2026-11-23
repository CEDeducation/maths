"""Original Grade 10 math lessons, organized by placement track. Run from project root."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

tracks=[
 {'id':'geometry','title':'Geometry','subtitle':'Think in shapes. Prove with confidence.','description':'Build a visual and logical foundation: angles, proof, congruence, similarity, circles and three-dimensional measurement.','color':'violet','icon':'Shapes','level':'Core • Geometry'},
 {'id':'algebra-2','title':'Algebra 2','subtitle':'Find the patterns behind the numbers.','description':'Go deeper into functions, quadratics, polynomials, radicals, exponentials and logarithms, with plenty of applied modeling.','color':'blue','icon':'FunctionSquare','level':'Core • Algebra 2'},
 {'id':'math-bridge','title':'Math Bridge','subtitle':'Go beyond the classroom.','description':'Extend your course with statistics, probability, the unit circle and precalculus skills used in IB MYP and honors pathways.','color':'mint','icon':'Atom','level':'Extension • MYP / Honors'},
]
chapters=[]; lessons=[]
def C(track,id,title,description):
    chapters.append(dict(id=id,trackId=track,title=title,description=description,order=sum(c['trackId']==track for c in chapters)+1))
def L(chapter,id,title,summary,ideas,formulas,worked,steps,mistake,application):
    lessons.append(dict(id=id,chapterId=chapter,title=title,summary=summary,ideas=ideas.split('|'),formulas=formulas.split('|'),workedExample=dict(prompt=worked,steps=steps.split('|')),commonMistake=mistake,realWorld=application,order=sum(x['chapterId']==chapter for x in lessons)+1,estimatedMinutes=18))

C('geometry','geo-foundations','Foundations & Proof','Learn the vocabulary and logic that turn a drawing into a mathematical argument.')
L('geo-foundations','points-lines-planes','Points, Lines & Planes','Geometry starts by describing locations and the objects connecting them. A point has no size; a line extends forever in both directions; a plane is a flat surface extending without end.',
 'Name a point with a capital letter, and a line using two points on it.|Two distinct points determine exactly one line; three noncollinear points determine exactly one plane.|Segments have two endpoints, while rays begin at one point and continue forever in one direction.',
 'Segment length on a number line = ∣b − a∣ |Midpoint = (a + b)/2',
 'Points A and B are at −3 and 7 on a number line. Find the length and midpoint of AB.',
 'Length = |7 − (−3)| = 10.|Midpoint = (−3 + 7)/2 = 2.|A segment is finite, even though its supporting line goes on forever.',
 'Do not confuse a segment with a full line; the segment has endpoints.','Map coordinates, architectural diagrams and computer graphics all rely on points and segments.')
L('geo-foundations','angles-parallel','Angles & Parallel Lines','Angles measure a turn between two rays. Parallel lines intersected by a transversal create repeating angle patterns.',
 'Vertical angles are equal; a linear pair sums to 180°.|Corresponding and alternate interior angles are equal when the lines are parallel.|Same-side interior angles are supplementary: their measures add to 180°.',
 'Complementary: a + b = 90°|Supplementary: a + b = 180°',
 'One alternate interior angle measures 68°. Find the matching angle when the lines are parallel.',
 'Identify the pair as alternate interior angles.|Parallel lines make alternate interior angles congruent.|The other angle is 68°.',
 'Adjacent does not always mean equal; check whether the angles are vertical, corresponding or supplementary.','Street grids and stair railings use parallel-line angle reasoning.')
L('geo-foundations','logic-proofs','Logic & Two-Column Proofs','A proof is a chain of statements, each supported by a definition, postulate or theorem. The goal is to explain why a result must be true.',
 'A conditional statement has hypothesis P and conclusion Q: if P, then Q.|Modus ponens says P and (P → Q) together imply Q.|In a two-column proof, the left column gives statements and the right column gives reasons.',
 'P → Q, P ⟹ Q|A = B, B = C ⟹ A = C',
 'Given AB = CD and CD = EF, prove AB = EF.',
 'Write AB = CD (given).|Write CD = EF (given).|Use the transitive property of equality: AB = EF.',
 'A drawing is not proof; properties must follow from stated facts.','Formal reasoning supports coding, science experiments and persuasive arguments.')

C('geometry','geo-triangles','Triangles & Congruence','Master triangle rules and justify when two triangles are exactly the same shape and size.')
L('geo-triangles','triangle-angles','Triangle Angle Relationships','The three interior angles of any triangle add to 180°. Exterior angles encode the two remote interior angles.',
 'Classify triangles as acute, right or obtuse by their angles.|The interior angle sum is 180° for every Euclidean triangle.|An exterior angle equals the sum of its two non-adjacent interior angles.',
 'A + B + C = 180°|Exterior angle = remote angle 1 + remote angle 2',
 'A triangle has angles 42° and 63°. Find its third angle.',
 'Add the known angles: 42 + 63 = 105°.|Subtract from 180°: 180 − 105 = 75°.|Check all three angles total 180°.',
 'Do not add 360°; that is the angle sum for a quadrilateral.','Surveyors use triangle-angle relationships to find inaccessible positions.')
L('geo-triangles','congruent-triangles','Triangle Congruence','Congruent triangles match in every side and angle. You rarely need all six measurements to prove it.',
 'SSS uses three pairs of matching sides.|SAS uses two sides and the included angle; ASA and AAS use corresponding angles and a side.|AAA proves similarity, not congruence; SSA is not a general congruence criterion.',
 'SSS, SAS, ASA, AAS, HL (right triangles)|CPCTC: corresponding parts of congruent triangles are congruent',
 'Two triangles have matching sides 5, 7 and 9. What makes them congruent?',
 'List three pairs of matching side lengths.|Apply the side-side-side criterion (SSS).|The corresponding angles must also match.',
 'SAS requires the INCLUDED angle, not any angle.','Engineers check congruent supports to ensure repeated components fit.')
L('geo-triangles','triangle-inequality','Triangle Inequality & Isosceles Triangles','Not every three lengths can create a triangle. Equal sides also reveal information about angles.',
 'The sum of any two side lengths must be greater than the third.|For ordered side lengths a ≤ b ≤ c, checking a + b > c is enough.|In an isosceles triangle, angles opposite equal sides are equal.',
 'a + b > c|Equal sides ⟺ equal opposite angles',
 'Can lengths 4, 6 and 9 form a triangle?',
 'Find the two shorter lengths: 4 and 6.|Their sum is 10, greater than 9.|Yes, the triangle inequality holds.',
 'Equality is not enough: 4 + 5 = 9 creates a straight segment, not a triangle.','Construction crews use bracing triangles because valid, rigid shapes matter.')

C('geometry','geo-similarity','Similarity & Right-Triangle Trigonometry','Connect scale factors, right-triangle distances and sine, cosine and tangent.')
L('geo-similarity','similar-triangles','Similarity & Scale Factor','Similar figures have equal corresponding angles and proportional matching side lengths. The scale factor changes distances but not shape.',
 'AA is enough to show two triangles are similar.|Match corresponding sides in the same order when writing proportions.|Perimeter scales by k, while area scales by k².',
 'new length = k × old length|new area = k² × old area',
 'A triangle with side 6 is enlarged by scale factor 2.5. Find the new side.',
 'Identify k = 2.5.|Multiply the side: 6 × 2.5 = 15.|Other corresponding sides use the same factor.',
 'Area does not scale by k; it scales by k².','Maps, blueprints and photo enlargements are all similarity models.')
L('geo-similarity','pythagorean-theorem','Pythagorean Theorem','A right triangle links its legs and hypotenuse through a beautiful square-area relationship.',
 'The hypotenuse is opposite the right angle and is the longest side.|For legs a and b and hypotenuse c, a² + b² = c².|Common triples include 3-4-5, 5-12-13 and scaled copies.',
 'a² + b² = c²|Distance = √((x₂−x₁)² + (y₂−y₁)²)',
 'A ladder reaches 12 feet up a wall and its foot is 5 feet away. How long is it?',
 'Identify the ladder as the hypotenuse.|Compute c² = 12² + 5² = 169.|Take the positive root: c = 13 feet.',
 'Do not treat the hypotenuse as a leg; it must be c.','Navigation, screens and building diagonals all use right-triangle distance.')
L('geo-similarity','right-triangle-trig','Sine, Cosine & Tangent','Trigonometric ratios connect an acute angle to lengths in a right triangle. You can find missing sides without knowing every angle.',
 'Relative to angle θ, identify opposite, adjacent and hypotenuse.|Sine is opposite/hypotenuse; cosine is adjacent/hypotenuse.|Tangent is opposite/adjacent; use inverse trig to find an angle.',
 'sin θ = opposite / hypotenuse|cos θ = adjacent / hypotenuse|tan θ = opposite / adjacent',
 'A right triangle has opposite side 3 and hypotenuse 5 relative to θ. Find sin θ.',
 'Locate the opposite and hypotenuse.|Use sin θ = opposite/hypotenuse.|sin θ = 3/5 = 0.6.',
 'Opposite and adjacent depend on the angle you choose.','Measure heights of trees or slopes of ramps from safe distances.')

C('geometry','geo-circles','Polygons & Circles','Use shape properties and circle geometry to solve visual and numerical problems.')
L('geo-circles','quadrilateral-properties','Quadrilaterals & Polygons','Polygons are closed figures of straight line segments. Their interior angle sums depend only on the number of sides.',
 'A quadrilateral has interior angle sum 360°.|Parallelograms have opposite sides parallel and equal, and opposite angles equal.|Rectangles have four right angles; rhombi have four equal sides; squares have both properties.',
 'Interior angle sum = (n − 2) × 180°|Regular polygon interior angle = (n − 2) × 180° / n',
 'Find the sum of interior angles of a hexagon.',
 'A hexagon has n = 6 sides.|Compute (6 − 2) × 180°.|The sum is 720°.',
 'A square is a rectangle and a rhombus, not a completely unrelated shape.','Floor tiles and roof trusses use polygon properties.')
L('geo-circles','circle-angles','Chords, Tangents & Circle Angles','Circle angles encode arcs. Central angles and inscribed angles that intercept the same arc follow a 2-to-1 relationship.',
 'A central angle has its vertex at the circle center.|An inscribed angle has its vertex on the circle and measures half its intercepted arc.|A radius to a point of tangency is perpendicular to the tangent line.',
 'Inscribed angle = intercepted arc / 2|Central angle = intercepted arc',
 'An inscribed angle intercepts an arc measuring 110°. Find the angle.',
 'Identify the intercepted arc measure, 110°.|An inscribed angle is half its intercepted arc.|110° / 2 = 55°.',
 'Do not halve the arc for a central angle: central angle and arc have equal measures.','Rotating parts and curved roadway designs depend on circular angles.')
L('geo-circles','arcs-sectors','Arc Length & Sector Area','A sector is a slice of a circle. Its arc length and area are fractions of the full circle determined by the central angle.',
 'Use degree fractions when the central angle is in degrees.|Circumference is 2πr, while circle area is πr².|For radian measure θ, arc length simplifies to rθ.',
 'Arc length = (θ/360°) × 2πr|Sector area = (θ/360°) × πr²',
 'Find the arc length of a 90° sector in a circle of radius 8.',
 'A 90° arc is one quarter of a full turn.|Full circumference is 2π(8) = 16π.|Arc length = 16π/4 = 4π.',
 'Arc length has distance units; sector area has square units.','Pizza portions, gears and irrigation sprinklers form sectors.')

C('geometry','geo-measurement','Area, Surface Area & Volume','Model two-dimensional and three-dimensional figures with the right units and formulas.')
L('geo-measurement','area-perimeter','Perimeter & Area','Perimeter measures distance around a figure; area counts the unit squares within it.',
 'Rectangle perimeter adds all four sides; its area multiplies length and width.|Triangle area uses half the base times the perpendicular height.|Circle circumference and area use π and radius.',
 'Rectangle area = lw; perimeter = 2(l+w)|Triangle area = bh/2|Circle area = πr²',
 'A rectangular garden is 8 meters by 5 meters. Find its area and perimeter.',
 'Area = 8 × 5 = 40 m².|Perimeter = 2(8 + 5) = 26 m.|Remember the units differ.',
 'The slanted side of a triangle is not always its height.','Garden design and flooring estimates require area and perimeter.')
L('geo-measurement','surface-area','Surface Area of Solids','Surface area adds the areas of all exposed faces of a solid. Net diagrams help make sure no face is missed.',
 'A rectangular prism has three pairs of equal opposing faces.|A cylinder has two circles and one curved lateral surface.|For pyramids and cones, distinguish slant height from vertical height.',
 'Prism SA = 2(lw + lh + wh)|Cylinder SA = 2πr² + 2πrh',
 'Find the surface area of a box measuring 2 by 3 by 4.',
 'Compute the three pair areas: 2×3, 2×4 and 3×4.|Add: 6 + 8 + 12 = 26.|Double for opposite faces: 52 square units.',
 'Do not confuse slant height with perpendicular height.','Packaging designers minimize material while covering every face.')
L('geo-measurement','volume-solids','Volume of Solids','Volume measures the space inside a three-dimensional figure. Recognize the cross-sectional base area first.',
 'A prism or cylinder volume equals base area × height.|Pyramids and cones have one-third the volume of their matching prism or cylinder.|A sphere volume is four-thirds π times radius cubed.',
 'Prism V = Bh|Cylinder V = πr²h|Cone V = πr²h/3|Sphere V = 4πr³/3',
 'Find the volume of a cylinder of radius 3 and height 5.',
 'Find circular base area: π×3² = 9π.|Multiply by height 5.|Volume = 45π cubic units.',
 'Volume uses cubic units, not square units.','Water tanks and storage containers are modeled by volume.')

C('algebra-2','alg-functions','Functions & Graphs','Understand the language of functions before studying their families.')
L('alg-functions','function-notation','Function Notation & Evaluation','A function assigns exactly one output to each input. Function notation makes it easy to describe and evaluate rules.',
 'f(x) means the output when input x is given; it is not multiplication f×x.|A vertical line test checks whether a graph is a function.|Inputs form the domain; resulting outputs form the range.',
 'If f(x) = 2x + 3, then f(4) = 11|Average rate of change = (f(b)−f(a))/(b−a)',
 'Given f(x) = 3x − 2, find f(5).',
 'Replace x with 5.|Calculate 3(5) − 2.|The output is 13.',
 'Substitute into the entire expression before simplifying.','Cost, distance and temperature rules can all be expressed as functions.')
L('alg-functions','graph-transformations','Graph Transformations','Transformations move or reshape a parent graph while preserving recognizable patterns.',
 'Adding outside the function shifts the graph vertically.|Replacing x by (x−h) shifts the graph RIGHT h units.|A negative outside the function reflects it over the x-axis.',
 'g(x) = a f(x−h) + k|Vertex of y=a(x−h)²+k is (h,k)',
 'Find the vertex of y = (x − 4)² + 3.',
 'Read h = 4 inside the parentheses.|Read k = 3 outside.|The vertex is (4,3).',
 'Horizontal shifts seem backwards: (x−4) means right 4.','Transform graphs to model growth, projectile paths and signals.')
L('alg-functions','function-composition','Composite Functions','Composition applies one function to the output of another. Order matters because f(g(x)) usually differs from g(f(x)).',
 'Compute the inside function first.|Use its output as the next function input.|For composition, check that the inside output belongs to the outer domain.',
 '(f∘g)(x) = f(g(x))|(g∘f)(x) = g(f(x))',
 'If f(x)=2x+1 and g(x)=x², find f(g(3)).',
 'Calculate g(3) = 3² = 9.|Use 9 as input to f: f(9)=2×9+1.|The answer is 19.',
 'Do not multiply f and g; the circle notation means compose.','Multi-stage pricing and unit conversion are function compositions.')

C('algebra-2','alg-quadratics','Quadratics & Complex Numbers','Solve second-degree equations and extend arithmetic to non-real solutions.')
L('alg-quadratics','factoring-quadratics','Factoring Quadratics','Factoring expresses a quadratic as a product of binomials, which can reveal its roots quickly.',
 'For x²+bx+c, find numbers that sum to b and multiply to c.|The zero-product property says AB=0 implies A=0 or B=0.|Always check the expression is equal to zero before reading roots.',
 'x² + bx + c = (x + p)(x + q), p+q=b, pq=c|AB=0 ⟹ A=0 or B=0',
 'Factor x² + 7x + 12 and solve x²+7x+12=0.',
 'Find 3 and 4 because 3+4=7 and 3×4=12.|Factor: (x+3)(x+4)=0.|Solutions are −3 and −4.',
 'Factoring an expression and solving an equation are different tasks.','Quadratic roots predict when trajectories reach ground level.')
L('alg-quadratics','solving-quadratics','Quadratic Formula & Discriminant','The quadratic formula solves any equation ax²+bx+c=0 with a≠0. The discriminant tells you what sort of roots to expect.',
 'First identify a, b and c with the equation written as zero.|The discriminant D=b²−4ac determines the number of real roots.|D>0 gives two distinct real roots, D=0 one repeated root, D<0 no real roots.',
 'x = (−b ± √(b²−4ac)) / (2a)|Discriminant D = b²−4ac',
 'Solve x² − 5x + 6 = 0.',
 'Set a=1, b=−5, c=6.|D=25−24=1.|x=(5±1)/2, giving x=2 or x=3.',
 'The denominator is 2a for the WHOLE numerator.','Projectile motion and revenue optimization involve quadratic models.')
L('alg-quadratics','complex-numbers','Introduction to Complex Numbers','Complex numbers extend real arithmetic using i, defined so i²=−1. They let us describe quadratic roots that are not real.',
 'A complex number has real part a and imaginary part b in a+bi.|Add real parts together and imaginary parts together.|Powers of i repeat every four steps: i, −1, −i, 1.',
 'i² = −1|i⁴ = 1|(a+bi)+(c+di)=(a+c)+(b+d)i',
 'Simplify (3+2i)+(4−5i).',
 'Add real parts: 3+4=7.|Add imaginary coefficients: 2+(−5)=−3.|Result: 7−3i.',
 'i is not the same as −1; i² equals −1.','Electrical engineering uses complex numbers to model alternating currents.')

C('algebra-2','alg-polynomials','Polynomial Functions','Analyze higher-degree expressions and their factor/graph relationships.')
L('alg-polynomials','polynomial-operations','Adding & Multiplying Polynomials','Polynomial operations combine like powers of x and use distribution to multiply every relevant term.',
 'Like terms have identical variable powers.|When multiplying monomials, add their exponents.|Multiply binomials with distribution, then combine like terms.',
 'xᵐ × xⁿ = xᵐ⁺ⁿ|(x+a)(x+b)=x²+(a+b)x+ab',
 'Expand (x+3)(x+5).',
 'Multiply each term: x²+5x+3x+15.|Combine the x terms.|Result: x²+8x+15.',
 'Do not add exponents when adding terms; only combine like powers.','Polynomial expressions model production and geometry relationships.')
L('alg-polynomials','polynomial-division','Synthetic Division & Factor Theorem','Division reveals whether a linear expression is a polynomial factor. Synthetic division is a compact method for x−c divisors.',
 'The Remainder Theorem says the remainder upon dividing P(x) by x−c equals P(c).|If P(c)=0, then x−c is a factor.|Write missing polynomial powers as zero coefficients before synthetic division.',
 'Remainder for P(x) ÷ (x−c) = P(c)|P(c)=0 ⟺ (x−c) is a factor',
 'For P(x)=x²−5x+6, is x−2 a factor?',
 'Evaluate P(2)=4−10+6=0.|The remainder is zero.|So x−2 is a factor.',
 'For a divisor x+3, synthetic input c is −3, not +3.','Factor tests help identify roots of higher-degree models.')
L('alg-polynomials','polynomial-end-behavior','End Behavior & Turning Points','A polynomial’s leading term controls how its graph behaves far left and far right.',
 'Even-degree polynomials point the same way at both ends.|Odd-degree polynomials point in opposite directions.|A positive leading coefficient makes the right end point up; a negative one makes it point down.',
 'Leading term = aₙxⁿ|Maximum turning points for degree n: n−1',
 'Describe the right-end behavior of f(x)=−2x³+5x+1.',
 'The leading term is −2x³.|Odd degree and negative coefficient give a falling right end.|As x→+∞, f(x)→−∞.',
 'Lower-degree terms do not control end behavior.','End behavior helps interpret long-range growth models.')

C('algebra-2','alg-rational','Rational & Radical Expressions','Work safely with fractions involving variables and equations involving square roots.')
L('alg-rational','rational-expressions','Simplifying Rational Expressions','Rational expressions are fractions of polynomials. Factoring often exposes common factors that can be canceled.',
 'Factor the numerator and denominator before canceling.|Only cancel common MULTIPLICATIVE factors, never terms separated by + or −.|Excluded inputs make the original denominator equal zero, even if a factor cancels.',
 '(x²−9)/(x−3)=x+3 for x≠3|denominator ≠ 0',
 'Simplify (x²−16)/(x−4).',
 'Factor numerator: (x−4)(x+4).|Cancel the common factor x−4.|The result is x+4, with x≠4.',
 '(x+2)/x does not simplify to 2; never cancel across addition.','Rates, mixture formulas and rational models use variable fractions.')
L('alg-rational','radical-equations','Radical Expressions & Equations','Radicals reverse powers, but squaring both sides can introduce answers that do not satisfy the starting equation.',
 '√x is the nonnegative principal square root.|Isolate the radical before squaring both sides.|Substitute candidate solutions into the ORIGINAL equation to reject extraneous roots.',
 '√a × √b = √(ab) for a,b≥0|If √(x+c)=d, then x=d²−c (check d≥0)',
 'Solve √(x+5)=4.',
 'Square both sides: x+5=16.|Solve x=11.|Check √16=4; the solution is valid.',
 'Squaring can add invalid solutions; always check.','Distance and energy formulas often contain square roots.')
L('alg-rational','rational-asymptotes','Rational Graphs & Asymptotes','A rational function can approach a line without touching it. Zeros of denominators and polynomial degrees predict its behavior.',
 'A vertical asymptote often occurs where a reduced denominator is zero.|If numerator degree is less than denominator degree, horizontal asymptote is y=0.|If degrees are equal, the horizontal asymptote is the ratio of leading coefficients.',
 'f(x)=a/(x−h)+k: VA x=h, HA y=k|Equal degrees: HA y = leading coefficient ratio',
 'Find the vertical asymptote of f(x)=3/(x−5)+2.',
 'Set the denominator x−5=0.|Solve x=5.|This is the vertical asymptote; y=2 is horizontal.',
 'A canceled denominator factor creates a hole, not necessarily a vertical asymptote.','Rational graphs describe saturation and inverse-distance behavior.')

C('algebra-2','alg-growth','Exponents, Logs & Sequences','Model repeated multiplication, undo exponentiation and recognize iterative patterns.')
L('alg-growth','exponential-functions','Exponential Growth & Decay','Exponential models multiply by the same factor over equal time intervals. This is different from adding a fixed amount.',
 'In y=a·bᵗ, a is the initial amount and b is the growth/decay factor.|For a growth rate r, b=1+r; for decay rate r, b=1−r.|Equal percentage change creates exponential rather than linear growth.',
 'A(t)=A₀(1+r)ᵗ|Decay: A(t)=A₀(1−r)ᵗ',
 'A population of 200 grows by 10% per year. Find the count after two years.',
 'Set growth factor b=1.10.|Compute 200×1.10².|The model gives 242.',
 '10% growth means multiply by 1.10, not add 10 each year.','Population, compound interest and bacterial growth are exponential.')
L('alg-growth','logarithms','Logarithms & Inverse Operations','A logarithm asks for the exponent required to reach a number. It is the inverse of exponentiation.',
 'log_b(x)=y means bʸ=x, with b>0 and b≠1.|The argument of a real logarithm must be positive.|Product, quotient and power rules simplify logarithmic expressions.',
 'log_b(xy)=log_b x+log_b y|log_b(xⁿ)=n log_b x|log_b(bˣ)=x',
 'Evaluate log₂(32).',
 'Ask: what exponent on 2 makes 32?|Since 2⁵=32, the exponent is 5.|Therefore log₂(32)=5.',
 'log(a+b) is NOT log a + log b.','The Richter-like scales and sound intensity use logarithmic scales.')
L('alg-growth','arithmetic-geometric-sequences','Arithmetic & Geometric Sequences','Sequences organize numbers by position. Arithmetic sequences add a constant; geometric sequences multiply by a constant.',
 'Arithmetic sequences have common difference d.|Geometric sequences have common ratio r.|For finite sums, use the number of terms and the right formula.',
 'Arithmetic aₙ=a₁+(n−1)d|Geometric aₙ=a₁rⁿ⁻¹|Arithmetic sum Sₙ=n(a₁+aₙ)/2',
 'Find term 6 of the arithmetic sequence 4, 7, 10, …',
 'The first term is 4 and common difference is 3.|Use a₆=4+(6−1)×3.|The sixth term is 19.',
 'The nth term uses n−1 jumps from the first term.','Savings plans and repeated patterns can be modeled as sequences.')

C('math-bridge','bridge-statistics','Statistics & Probability','Make sense of data and calculate the likelihood of outcomes.')
L('bridge-statistics','center-spread','Mean, Median & Standard Deviation','Summary measures describe the center and spread of a data set. Different measures answer different questions.',
 'Mean is the arithmetic average; median is the middle after sorting.|Range is maximum minus minimum; outliers influence mean more than median.|Standard deviation measures typical distance from the mean in the same units as data.',
 'Mean = Σx / n|Range = max − min|Population variance = Σ(x−μ)²/n',
 'Find the mean and range of 3, 5, 7, 9.',
 'Sum values: 3+5+7+9=24.|Divide by four: mean=6.|Range=9−3=6.',
 'The median cannot be identified reliably without sorting first.','Teams use statistics to evaluate performance and compare populations.')
L('bridge-statistics','counting-principles','Permutations & Combinations','Counting techniques avoid writing every possible arrangement. The key question is whether order matters.',
 'Use the multiplication principle for independent stages.|Permutations count ordered arrangements; combinations count unordered selections.|Factorial n! multiplies every positive integer up to n, and 0!=1.',
 'nPᵣ=n!/(n−r)!|nCᵣ=n!/(r!(n−r)!)',
 'How many ways can you choose 2 captains from 5 students when order does not matter?',
 'This is a combination because the selected pair has no order.|Compute 5C2 = (5×4)/(2×1).|There are 10 distinct pairs.',
 'A team selection uses combinations; assigning president and vice president uses permutations.','Event planning and probability calculations depend on counting.')
L('bridge-statistics','conditional-probability','Conditional Probability','Conditional probability revises the sample space using information you already know.',
 'P(A∣B) means probability of A given B happened.|For equally likely outcomes, compare the overlap with the size of B.|Independent events satisfy P(A∣B)=P(A), when P(B)>0.',
 'P(A∣B) = P(A∩B)/P(B)|P(A∩B)=P(A∣B)P(B)',
 'From 12 students, 5 play soccer, and 3 of those 5 also play chess. Find P(chess | soccer).',
 'Restrict attention to the 5 soccer players.|Count the 3 who also play chess.|Probability is 3/5 = 60%.',
 'The denominator for P(A∣B) is the size/probability of B, not the entire group.','Medical testing and everyday risk estimates use conditional probability.')

C('math-bridge','bridge-trig','Unit Circle & Trigonometric Laws','Extend right-triangle trigonometry to all angles and non-right triangles.')
L('bridge-trig','unit-circle','Radian Measure & Unit Circle','The unit circle turns trigonometry into coordinates, making sine and cosine meaningful for any rotation.',
 'A full turn is 2π radians or 360°.|At angle θ on the unit circle, the coordinate is (cos θ, sin θ).|Quadrant signs determine whether sine and cosine are positive or negative.',
 'radians = degrees × π/180|degrees = radians × 180/π|Unit circle point = (cos θ, sin θ)',
 'Convert 150° to radians.',
 'Multiply by π/180.|150π/180 simplifies to 5π/6.|150° = 5π/6 radians.',
 'Radians are not degrees; use the correct calculator mode.','Waves, rotations and periodic motion use radians.')
L('bridge-trig','law-sines','Law of Sines','The Law of Sines relates side lengths to the sines of their opposite angles in any triangle.',
 'Use the law when you know a side and its opposite angle.|Match lowercase side a to uppercase opposite angle A.|The SSA case can sometimes produce two possible triangles.',
 'a/sin A = b/sin B = c/sin C|A+B+C=180°',
 'If side a=10 opposite A=30°, find side b opposite B=90°.',
 'Set b/sin90° = 10/sin30°.|Use sin90°=1 and sin30°=1/2.|b = 10/(1/2) = 20.',
 'Never pair a side with an angle that is not opposite it.','Triangulation can find distances between landmarks.')
L('bridge-trig','law-cosines','Law of Cosines','The Law of Cosines generalizes the Pythagorean theorem to triangles without a right angle.',
 'Use it with two sides and the included angle (SAS), or all three sides (SSS).|The cosine correction accounts for the included angle.|At 90°, cos90°=0, so it becomes the Pythagorean theorem.',
 'c² = a²+b²−2ab cos C|cos C=(a²+b²−c²)/(2ab)',
 'Two sides of a triangle are 5 and 7 with included angle 60°. Find the opposite side.',
 'Use c²=5²+7²−2×5×7×cos60°.|cos60°=1/2, so c²=25+49−35=39.|The length is √39 ≈ 6.24.',
 'The angle must be between the two provided sides for SAS use.','Navigation uses this rule to estimate distance between two travel legs.')

C('math-bridge','bridge-functions','Precalculus Function Skills','Read challenging function restrictions and transform formulas into models.')
L('bridge-functions','domain-range','Domain, Range & Restrictions','The domain is the set of allowed inputs; the range is the set of attained outputs. Algebraic operations can restrict inputs.',
 'A real square-root expression requires its radicand to be nonnegative.|A denominator cannot equal zero.|For quadratics in vertex form, the vertex helps identify the range.',
 '√(x−a) requires x≥a|1/(x−a) requires x≠a|y=(x−h)²+k has range y≥k',
 'Find the real domain of f(x)=√(x−4).',
 'Require the radicand x−4≥0.|Solve the inequality to get x≥4.|Domain is [4, ∞).',
 'A rational hole can remain excluded even if you cancel a factor.','Domain restrictions keep scientific models physically meaningful.')
L('bridge-functions','inverse-functions','Inverse Functions','An inverse reverses what a one-to-one function does. Inputs and outputs exchange places.',
 'A function needs to be one-to-one on its domain to have an inverse function.|To find an inverse, write y=f(x), swap x and y, then solve for y.|The graph of the inverse reflects across y=x.',
 'f⁻¹(f(x))=x (on the allowed domain)|If f(x)=ax+b, f⁻¹(x)=(x−b)/a, a≠0',
 'Find the inverse of f(x)=3x+6.',
 'Write y=3x+6 and swap x,y: x=3y+6.|Solve: y=(x−6)/3.|Thus f⁻¹(x)=(x−6)/3.',
 'f⁻¹(x) means inverse function, not 1/f(x).','Currency conversion and encoding/decoding use inverse relationships.')
L('bridge-functions','transformations-modeling','Function Modeling & Composition','Applied problems rarely announce the function to use. First identify relationships, inputs, units and restrictions.',
 'Translate a story into a rule and define what x represents.|Check units and sensible domain restrictions.|To connect two processes, compose their functions in the right order.',
 'Cost C(n)=fixed cost+(price per item)n|Revenue R(n)=unit price×quantity|Profit P(n)=R(n)−C(n)',
 'A bike rental charges $8 plus $3 per hour. Find the cost for 5 hours.',
 'Write C(h)=8+3h.|Substitute h=5: C(5)=8+15.|Total cost is $23.',
 'Always include the fixed starting cost; it is the y-intercept.','Budgeting, transportation and pricing provide natural function models.')

assert len(tracks)==3 and len(chapters)==13 and len(lessons)==39
assert all(len(x['ideas'])>=3 and len(x['workedExample']['steps'])>=3 for x in lessons)
(ROOT/'data'/'curriculum.json').write_text(json.dumps({'tracks':tracks,'chapters':chapters,'lessons':lessons},ensure_ascii=False,indent=2),encoding='utf-8')
print('Wrote',len(chapters),'chapters and',len(lessons),'lessons')
