{{ self.title() }}

{{ s('description') }}

给定两个整数 $a$ 和 $b$，请计算它们的和。

{{ s('input format') }}

{{ self.input_file() }}

输入仅一行，包含两个整数 $a$ 和 $b$，用一个空格分隔。

{{ s('output format') }}

{{ self.output_file() }}

输出一行，包含一个整数，表示 $a+b$。

{{ s('sample', 1) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

$1+2=3$。

{{ s('sample', 2) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

$-5+8=3$。

{{ s('sample', 3) }}

{{ self.sample_text() }}

{{ self.title_sample_description() }}

$1000000000+1000000000=2000000000$。

{{ s('subtasks') }}

对于所有测试数据，${{ args['min_value'].hn() }} \le a,b \le {{ args['max_value'].hn() }}$。