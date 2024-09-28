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


add_action('woocommerce_order_status_completed', 'send_order_details_to_email', 10, 1);

function send_order_details_to_email($order_id) {
    // 获取订单对象
    $order = wc_get_order($order_id);

    // 获取订单详情
    $order_data = $order->get_data();

    // 设置接收邮件的邮箱地址
    $to = 'battlebuns@163.com';

    // 设置邮件标题
    $subject = '订单完成通知 - 订单号: ' . $order_id;

    // 设置邮件内容
    $message = '订单详情：' . PHP_EOL;
    $message .= '订单号: ' . $order_id . PHP_EOL;
    $message .= '订单总额: ' . $order_data['total'] . PHP_EOL;
    $message .= '客户邮箱: ' . $order_data['billing']['email'] . PHP_EOL;
    $message .= '订单状态: ' . $order_data['status'] . PHP_EOL;

    // 获取订单中的商品信息
    $message .= '商品信息：' . PHP_EOL;
    foreach ($order->get_items() as $item_id => $item) {
        $product_id = $item->get_product_id();
        $message .= '商品ID: ' . $product_id . PHP_EOL;
        $product_name = $item->get_name();
        $quantity = $item->get_quantity();
        $message .= $product_name . ' x ' . $quantity . PHP_EOL;
    }

   // 获取并添加 API Key
    //$api_key = get_post_meta($order_id, 'api_key', true); // 尝试获取自定义字段
	$order = wc_get_order($order_id);
	$api_key = $order->get_meta('api_key');

    if (!empty($api_key)) {
        $message .= 'API Key: ' . $api_key . PHP_EOL; // 添加 API Key 到邮件内容
    } else {
        // 尝试从订单的自定义字段中提取 API Key
        $custom_fields = $order->get_meta('API-KEY'); // 可能需要调整为实际存储的键名
        if (!empty($custom_fields)) {
            $message .= 'API Key: ' . $custom_fields . PHP_EOL; // 添加到邮件内容
        } else {
            $message .= 'API Key: 未找到' . PHP_EOL; // 添加调试信息
        }
    }

    switch ($product_id) {
        case 71: // 假设产品 ID 为 71 的商品需要发出特定请求
            $api_url = 'http://1.94.120.213:5000/api/enlongkey';
            break;
        case 111: // 假设产品 ID 为 72 的商品需要发出另一个请求
            $api_url = 'http://1.94.120.213:5000/api/moremoney';
            break;
        // 可以添加更多商品 ID 和相应的请求逻辑
        default:
            break;// 如果没有匹配的商品 ID，则跳过该商品   
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

    // 设置邮件头部
    $headers = array('Content-Type: text/plain; charset=UTF-8');

    // 发送邮件
    wp_mail($to, $subject, $message, $headers);
	
	
	
	    // 如果 API Key 存在，则请求 /api/renew
    if ($api_key) {
        $url = 'http://1.94.120.213:5000/api/renew'; // 替换为你的 API URL
        $dollar = 10; // 固定的 dollar 值

        // 准备 POST 请求的数据
        $data = array(
            'apikey' => $api_key,
            'dollar' => $dollar,
            'date' => date('2024年12月31日') // 可以根据需要格式化日期
        );

	    // 使用 wp_remote_post 发送 POST 请求
        $response = wp_remote_post($url, array(
            'method'    => 'POST',
            'body'      => json_encode($data),
            'headers'   => array('Content-Type' => 'application/json'),
        ));
		
		
		if (is_wp_error($renew_response)) {
            // 处理错误
            $message .= 'Renew request failed: ' . $renew_response->get_error_message() . PHP_EOL;
        } else {
            $renew_data = json_decode(wp_remote_retrieve_body($renew_response), true);

            // 发送 api/query 请求
            $query_response = wp_remote_post('http://1.94.120.213:5000/api/query', array(
                'method'    => 'POST',
                'body'      => json_encode(array(
                    'apikey' => $api_key,
                )),
                'headers'   => array('Content-Type' => 'application/json'),
            ));

            if (is_wp_error($query_response)) {
                // 处理错误
                $message .= 'Query request failed: ' . $query_response->get_error_message() . PHP_EOL;
            } else {
                $query_data = json_decode(wp_remote_retrieve_body($query_response), true);

                // 添加 query_data 信息到邮件内容
                $message .= 'API Key 使用情况：' . PHP_EOL;
                $message .= '已用次数: ' . $query_data['used_count'] . PHP_EOL;
                $message .= '剩余次数: ' . $query_data['remaining_count'] . PHP_EOL;
                $message .= '创建日期: ' . $query_data['creation_date'] . PHP_EOL;
                $message .= '截止日期: ' . $query_data['expiration_date'] . PHP_EOL;
            }
        }
	}
	
}




add_action('woocommerce_checkout_after_order_review', 'display_api_usage_info');

function display_api_usage_info() {
    // 获取当前用户的 API Key（假设已存储在用户的元数据中）
//     $user_id = get_current_user_id();
//     $api_key = get_user_meta($user_id, 'api_key', true);
    $order = wc_get_order($order_id);
	$api_key = $order->get_meta('api_key');
    if ($api_key) {
        // 发送 api/query 请求获取 API 使用情况
        $query_response = wp_remote_post('http://1.94.120.213:5000/api/query', array(
            'method'    => 'POST',
            'body'      => json_encode(array(
                'apikey' => $api_key,
            )),
            'headers'   => array('Content-Type' => 'application/json'),
        ));

        if (!is_wp_error($query_response)) {
            $query_data = json_decode(wp_remote_retrieve_body($query_response), true);
            echo '<div class="api-usage-info">';
            echo '<h3>API 使用情况</h3>';
            echo '<p>已用次数: ' . esc_html($query_data['used_count']) . '</p>';
            echo '<p>剩余次数: ' . esc_html($query_data['remaining_count']) . '</p>';
            echo '<p>创建日期: ' . esc_html($query_data['creation_date']) . '</p>';
            echo '<p>截止日期: ' . esc_html($query_data['expiration_date']) . '</p>';
            echo '</div>';
        }
    }
}
