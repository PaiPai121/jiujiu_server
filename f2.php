<?php
/**
 * Blocksy functions and definitions
 *
 * @link https://developer.wordpress.org/themes/basics/theme-functions/
 *
 * @package Blocksy
 */

if (version_compare(PHP_VERSION, '5.7.0', '<')) {
	require get_template_directory() . '/inc/php-fallback.php';
	return;
}

require get_template_directory() . '/inc/init.php';


add_action('woocommerce_order_status_completed', 'handle_api_key_request_after_order', 10, 1);

function handle_api_requests_after_order($order_id) {
    // 获取当前订单对象
    $order = wc_get_order($order_id);
    // 获取订单详情
    $order_data = $order->get_data();
	// 获取并添加 API Key
    //$api_key = get_post_meta($order_id, 'api_key', true); // 尝试获取自定义字段
	$order = wc_get_order($order_id);
	$api_key = $order->get_meta('api_key');
    // 遍历订单中的商品
    foreach ($order->get_items() as $item_id => $item) {
        $product_id = $item->get_product_id();
        $quantity = $item->get_quantity();
        
        // 根据产品 ID 指定不同的 API Key 和请求 URL
        switch ($product_id) {
            case 71: // 假设产品 ID 为 71 的商品需要发出特定请求
                // $api_key = $api_key; // 从商品元数据或其他地方获取相应的 API Key
                $api_url = 'http://1.94.120.213:5000/api/enlongkey';
                break;
            case 111: // 假设产品 ID 为 72 的商品需要发出另一个请求
                // $api_key = 'YOUR_API_KEY_FOR_PRODUCT_111';
                $api_url = 'http://1.94.120.213:5000/api/moremoney';
                break;
            // 可以添加更多商品 ID 和相应的请求逻辑
            default:
                continue 2; // 如果没有匹配的商品 ID，则跳过该商品
        }

        // 发送请求
        $response = wp_remote_post($api_url, array(
            'method'    => 'POST',
            'body'      => json_encode(array(
                'apikey' => $api_key,
                'quantity' => $quantity, // 如果需要传递数量
            )),
            'headers'   => array('Content-Type' => 'application/json'),
        ));

//         if (!is_wp_error($response)) {
//             $response_data = json_decode(wp_remote_retrieve_body($response), true);
//             // 处理 API 返回的数据
//             echo '<div class="api-response-info">';
//             echo '<h3>API 响应 for Product ID ' . esc_html($product_id) . '</h3>';
//             echo '<p>响应数据: ' . esc_html(json_encode($response_data)) . '</p>';
//             echo '</div>';
//         }
    }
}



add_filter('woocommerce_quantity_input_args', 'set_max_quantity_to_one', 10, 2);
function set_max_quantity_to_one($args, $product) {
    $args['max_value'] = 1;  // 设置最大购买数量为 1
    $args['min_value'] = 1;   // 设置最小购买数量为 1
    return $args;
}
