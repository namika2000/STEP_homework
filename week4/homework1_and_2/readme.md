# HOMEWORK1

## 他の関数で呼び出す関数

### get_ID_from_title(self, target)
ページタイトルを受け取り、対応するページIDを返す

### return_shortest_path(self, node_pair: dict[int: list[int]], goal: int) -> list[int]
最短経路までに探索したノードたちを辿り、startからgoalまでの最短経路を返す

0. node_pair_dequeとshortest_pathを用紙し, targetにgoalを代入
    * node_pair_deque: (node, [child1, child2,...])を要素する配列
    * shortest_path: 最短経路を格納するための配列
1. node_pair_dequeをgoalからstartまで逆順に辿る
    1. もしtargetとなるページがnodeのchild配列に存在すればshortest_pathの先頭にそのnodeを格納
        * 先頭に格納することで最終的にstartからgoalまでが順番に並ぶため
2. find_shortest_pathを返す

## メイン関数
### find_shortest_path(self, start, goal)
開始/終了のページタイトルを受け取り、それらの最短経路を返す
ページランクが高いページを求める

0.  enqueued_node_pair, visited_nodes, deque_list, is_foundを用意
    * enqueued_node_pair: enqueueしたノードたちの親子関係. 
        * ex: {node:[child1, child2], child1: [child3, child4]}
    * visited_nodes: {node: enqueueされたかどうか}
        * 初めはkeyがstart以外のvalueがFalse
    * deque_list: 探索するノードを入れるdeque. 初めにstartを入れておく
    * is_found: goalが見つかったかどうか
1. dequeリストに要素があり、かつis_foundがFalseである限り以下を実行
    1. nodeにdeque_listの先頭の要素を代入
    2. nodeのchildを順番に見ていく
        1. visited_nodesにchildがあるか判定
            * あれば
                * スキップ
            * なければ
                * deque_listにchildを加え、visited_nodes[child]をTrueに
                * enqueued_node_pair[node]にchildを加える
                * もしchildがgoalならそこでループを抜ける
2. 最短経路をページIDからページタイトルに直して出力


# HOMEWORK2

## メイン関数
### find_most_popular_pages(self)
全ノードのページランクを収束するまで計算する

0. page_rank_child, page_rank_parent, threshold, number_of_nodes, sum_of_page_rank, diffを用意
    * page_rank_child: 更新後のページランク. 親から振り分けれるランクの総和が入る
      * {child: page_rank}
    * page_rank_parent: 元のページランク. 親のページランク
    * threshold: 更新の前後でページランクの差がこれ以下なら収束とする
    * number_of_nodes: 全ノードの数
    * sum_of_page_rank: ページランクの総和. 更新の前後で一定
    * diff: 更新の前後でのページランクの差
1. diff > thresholdの間は以下を実行
    1. 全てのノードに0.15を割り当てる
        1. そのノードがchildを持つかどうかで分岐
            * 持たないなら
                * そのノードのページランクの85%を全ノードに均等に割り当てる
            * 持つなら
                * そのノードのページランクの85%を子ノードに均等に割り当てる
    2. 更新の前後でのページランクの差diffを比較
        * もしdiffがthreshold以下ならループを抜ける
    3. 次の計算のための準備
        * page_rank_parent[node]にpage_rank_child[node]を代入
        * page_rank_child[node]を0に初期化
2. ページランクが収束したら、最もページランクが高いページを求める
3. 結果を出力