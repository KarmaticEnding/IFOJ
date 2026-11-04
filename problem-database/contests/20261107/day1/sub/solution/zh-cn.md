{{ self.title() }}

$$
\begin{align*}
& \sum_{i = l}^{r} \sum_{j = i}^{r} \sum_{k = i}^{j} a_k \\
= & \sum_{k = l}^{r} a_k \sum_{i = l}^{k} \sum_{j = k}^{r} 1 \\
= & \sum_{k = l}^{r} a_k (k - l + 1)(r - k + 1) \\
= & \sum_{k = l}^{r} -k^2a_k + (l + r)ka_k - (l - 1)(r + 1)a_k \\
= & -\sum_{k = l}^{r} k^2a_k + (l + r)\sum_{k = l}^{r} ka_k - (l - 1)(r + 1)\sum_{k = l}^{r} a_k
\end{align*}
$$

线段树每个结点维护对应区间的 $\sum k^2a_k, \sum ka_k, \sum a_k$ 即可。

由于每个区间的 $\sum k^2, \sum k$ 容易计算，所以区间加可以用可下传标记的线段树来维护。