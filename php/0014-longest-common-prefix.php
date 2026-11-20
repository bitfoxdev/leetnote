class Solution {

    /**
     * @param String[] $strs
     * @return String
     */
    function longestCommonPrefix($strs) {
        if (empty($strs)) {
            return "";
        }

        $first = $strs[0];
        $len = strlen($first);

        for ($i = 0; $i < $len; $i++) {
            $char = $first[$i];
            for ($j = 1; $j < count($strs); $j++) {
                if ($i === strlen($strs[$j]) || $strs[$j][$i] !== $char) {
                    return substr($first, 0, $i);
                }
            }
        }

        return $first;
    }
}
