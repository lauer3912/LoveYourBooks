# Alternative notation for exponents, logs and roots?

If we have

\\[
x^y = z
\\]

then we know that

\\[
\sqrt[y]{z} = x
\\]

and

\\[
\log_x{z} = y .
\\]

## Maybe

Always assuming x>0 and z>0, how about:

<p>
\begin{align}
x^y &={} \stackrel{y}{_x\triangle_{\phantom{z}}}&&\text{$x$ to the $y$}\\
\sqrt[y]{z} &={} \stackrel{y}{_\phantom{x}\triangle_{z}}&&\text{$y$th root of $z$}\\
\log_x(z)&={} \stackrel{}{_x\triangle_{z}}&&\text{log base $x$ of $z$}\\
\end{align}
</p>

<p>
The equation $x^y = z$ is sort of like the complete triangle $\stackrel{y}{_x\triangle_{z}}$.
If one vertex of the triangle is left blank, the net value of the expression is the value needed to fill in that blank. This has the niceness of displaying the trinary relationship between the three values. Also, the left-to-right flow agrees with the English way of verbalizing these expressions. It does seem to make inverse identities awkward:
<ul>
    <li>
$\log_x(x^y)=y$
becomes
$\stackrel{}{_x\triangle_{\stackrel{y}{_x\triangle_{\phantom{z}}}}}=y$.
(Or you could just say
$\stackrel{}{_x\stackrel{y}{\triangle}_{\stackrel{y}{_x\triangle_{\phantom{z}}}}}$
)
    </li>
    <li>
$x^{\log_x(z)}=z$
becomes
$\stackrel{\stackrel{}{_x\triangle_{z}}}{_x\triangle_{\phantom{z}}}=z$.
(Or you could just say 
$\stackrel{\stackrel{}{_x\triangle_{z}}}{_x\triangle_{z}}$
).
    </li>
    <li>
$\sqrt[y]{x^y}=x$
becomes
$\stackrel{y}{\triangle}_{\stackrel{y}{_x\triangle_{\phantom{z}}}}=x$.
(Or you could just say 
$\stackrel{}{_x\stackrel{y}{\triangle}_{\stackrel{y}{_x\triangle_{\phantom{z}}}}}$ 
again.)
    </li>
    <li>
$(\sqrt[y]{z})^y=z$ 
becomes 
$_{\stackrel{y}{_\phantom{x}\triangle_{z}}}\hspace{-.25pc}\stackrel{y}{\triangle}=z$.
(Or you could just say 
$_{\stackrel{y}{_\phantom{x}\triangle_{z}}}\hspace{-.25pc}\stackrel{y}{\triangle}_z$
.)
    </li>
</ul>
</p>

(I am sure that there must be better ways to typeset these, but this is what I could come up with.)
Having **3** variables, I was sure that there must be 3! identities, but at first I could only come up with these four. Then I noticed the similarities in structure that these four have: in each case, the larger $\triangle$ uses one vertex (say vertex A) for a simple variable. A second vertex (say vertex B) has a smaller $\triangle$ with the same simple variable in its vertex A. The smaller $\triangle$ leaves vertex B empty and makes use of vertex C.

<p>
<ul class="CustomMathTextLeftAlgin_Display">
    <li><strong>
$$\stackrel{a}{_x\triangle_{\phantom{z}}}\cdot\stackrel{b}{_x\triangle_{\phantom{z}}}={}\stackrel{a+b}{_x\triangle_{\phantom{z}}}$$
    </strong></li>
    <li><strong>
$$\frac{\stackrel{a}{_x\triangle_{\phantom{z}}}}{\stackrel{b}{_x\triangle_{\phantom{z}}}}={}\stackrel{a-b}{_x\triangle_{\phantom{z}}}$$
    </strong></li>
    <li><strong>
$$_{\stackrel{a}{_x\triangle_{\phantom{z}}}}\hspace{-.25pc}\stackrel{b}{\triangle}={}\stackrel{ab}{_x\triangle_{\phantom{z}}}$$
    </strong></li>
    <li><strong>
$$\stackrel{}{_x\triangle_{ab}}={}\stackrel{}{_x\triangle_{a}}+\stackrel{}{_x\triangle_{b}}$$
    </strong></li>
    <li><strong>
$$\stackrel{}{_x\triangle_{a/b}}={}\stackrel{}{_x\triangle_{a}}-\stackrel{}{_x\triangle_{b}}$$
    </strong></li>
    <li><strong>
$$\stackrel{}{_x\triangle}_{\stackrel{b}{_a\triangle_{\phantom{z}}}}=b\cdot\stackrel{}{_x\triangle}_{a}$$
    </strong></li>
    <li><strong>
$$\stackrel{-a}{_x\triangle_{\phantom{z}}}=\frac{1}{\stackrel{a}{_x\triangle_{\phantom{z}}}}$$
    </strong></li>
    <li><strong>
$$\stackrel{1/y}{_x\triangle_{\phantom{z}}}=\stackrel{y}{_\phantom{x}\triangle_{x}}$$
    </strong></li>
    <li><strong>
$$\stackrel{}{_x\triangle_{1/a}}=-\mathord{\stackrel{}{_x\triangle_{a}}}$$
    </strong></li>
    <li><strong>
$$\stackrel{}{_a\triangle_{b}}\cdot\stackrel{}{_b\triangle_{c}}=\stackrel{}{_a\triangle_{c}}$$
    </strong></li>
    <li><strong>
$$\stackrel{}{_a\triangle_{c}}=\frac{\stackrel{}{_b\triangle_{c}}}{\stackrel{}{_b\triangle_{a}}}$$
    </strong></li>
</ul>
</p>
