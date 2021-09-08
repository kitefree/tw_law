<?php
include_once("db_con.php");
header('Access-Control-Allow-Origin:*');

function sql_where($kw)
{
    $where  = " AND ( ";
    //$where .= " AA013 LIKE '%{$kw}%' ";
    //$where .= " OR AA014 LIKE '%{$kw}%' ";
    $where .= " AA004 LIKE '%{$kw}%' ";
    $where .= " ) ";
    return $where;
}

function search_autoComplete()
{
    $kw = $_GET['txtkw'];

    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
    
    
    $sql = "
    SELECT AA004
    FROM LAWAA 
    WHERE 1=1 
    AND AA004 LIKE '%{$kw}%' LIMIT 5";
    $result = $link->query($sql);
    
    $arr_json = array();
    while($row =mysqli_fetch_assoc($result))
    {
        $arr_json[] = $row;
    }
    
    mysqli_close($link);
    
    //echo $_GET['txtkw'];
    echo json_encode($arr_json);
}

//首頁 法規查詢
function search_query_AA()
{
    $kw = $_GET['txtkw'];

    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
    
    
    $sql = "
    SELECT AA001,AA002,AA004,AA007,'head' as TYPE
    FROM LAWAA 
    WHERE 1=1 
    AND AA004 LIKE '%{$kw}%'";
    $result = $link->query($sql);
    
    $arr_json = array();
    while($row =mysqli_fetch_assoc($result))
    {
        $arr_json[] = $row;
    }
    
    mysqli_close($link);
    
    //echo $_GET['txtkw'];
    echo json_encode($arr_json);
}

//首頁 法條查詢
function search_query_AC()
{
    $kw = $_GET['txtkw'];

    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
 
    $sql = "
    SELECT DISTINCT AC002,AC003,AC006,AC007,AC008,'body' as TYPE
    FROM LAWAC
    WHERE 1=1
    AND REPLACE(REPLACE(AC011,'\r\n',''),' ','') LIKE '%{$kw}%';";

    $result = $link->query($sql);

    $arr_json = array();
    while($row =mysqli_fetch_assoc($result))
    {
        $arr_json[] = $row;
    }
    
    mysqli_close($link);
    
    //echo $_GET['txtkw'];
    echo json_encode($arr_json);
}

//LawAll 單頭查詢
function law_aa_query(){
    $AA002 = $_GET['AA002'];
    
    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
    
    
    $sql = "
    SELECT * 
    FROM LAWAA     
    WHERE AA002='{$AA002}'";    
    $result = $link->query($sql);
    
    $arr_json = array();
    while($row =mysqli_fetch_assoc($result))
    {
        $arr_json[] = $row;
    }

    mysqli_close($link);
    
    echo json_encode($arr_json);
}



function law_ab_query()
{
    $AA002 = $_GET['AA002'];
    
    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
    
    
    $sql = "
    SELECT AB001,AB002,AB003,AB005
    FROM LAWAB    
    WHERE AB002='{$AA002}'
    ORDER BY AB003";

    $result = $link->query($sql);
    
    $arr_json = array();
    while($row =mysqli_fetch_assoc($result))
    {
        $arr_json[] = $row;
    }

    mysqli_close($link);
    
    echo json_encode($arr_json);
}

//LawAll 單身查詢
function law_ac_query_all(){
    $AA002 = $_GET['AA002'];
    
    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
    $sql_1 = "SELECT COUNT(AB002) as cnt FROM `LAWAB` WHERE AB002='{$AA002}';";
    $result = $link->query($sql_1);
    $row = mysqli_fetch_array($result);

    if($row[0] == '0'){
        $sql_2 = "
        SELECT '' AS AA003, '' AS AA004
        ,'' AS AB002,'' AS AB003
        ,'' AS AB005
        ,AC005
        ,AC010
        ,AC011        
        FROM `LAWAC` WHERE AC003='{$AA002}';
        ";
    }
    else{
        $sql_2 = "
        SELECT AA003,AA004
        ,AB002,AB003
        ,AB005
        ,AC006
        ,AC010
        ,AC011
        FROM LAWAA 
        LEFT JOIN LAWAB ON AA002 = AB002
        LEFT JOIN LAWAC ON AC003 = AA002 AND AC004 = AB003
        WHERE AA002='{$AA002}'
        ORDER BY AB003
        ,CAST(SUBSTRING_INDEX(AC005,'-', 1) AS UNSIGNED) ASC
        ,CASE WHEN LOCATE('-',AC005) >0 THEN CAST(SUBSTRING_INDEX(AC005,'-', -1) AS UNSIGNED) ELSE 0 END ASC";        
    }

    
    $result = $link->query($sql_2);
    

    $prior_AB005 = '';
    while($row =mysqli_fetch_assoc($result))
    {
        if($prior_AB005 == '')
        {
            $arr_json[] = $row;
            $prior_AB005 = $row['AB005'];
        }
        else if($row['AB005'] == $prior_AB005)
        {
            $row['AB005'] = '';
            $arr_json[] = $row;
        }
        else if($row['AB005'] != $prior_AB005){
            $arr_json[] = $row;
            $prior_AB005 = $row['AB005'];
        }
    }

    mysqli_close($link);
    
    echo json_encode($arr_json);
}

//LawAll 單身查詢
function law_ac_query_single(){
    $AA002 = $_GET['AA002'];
    $AC011 = $_GET['AC011'];
    
    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);    

    $sql = "
    SELECT AC001,AC002,AC003,AC004,AC005,AC006,AC007,AC008,AC009,AC010,AC011
    FROM LAWAC 
    WHERE AC003='{$AA002}' 
    AND REPLACE(REPLACE(AC011,'\r\n',''),' ','') LIKE '%{$AC011}%';";  

    $result = $link->query($sql);

    $arr_json = array();
    while($row =mysqli_fetch_assoc($result))
    {
        $arr_json[] = $row;
    }

    mysqli_close($link);
    
    echo json_encode($arr_json);
}


$api = $_GET['api'];


switch($api){
    case 'search_autoComplete':
        search_autoComplete();
        break;
    case 'search_query_AA':
        search_query_AA();
        break;
    case 'search_query_AC':
        search_query_AC();
        break;        
    case 'law_aa_query':
        law_aa_query();
        break;         
    case 'law_ac_query_all':
        law_ac_query_all();
        break;
    case 'law_ac_query_single':
        law_ac_query_single();
        break;         
}

// echo $where;
// exit;





//print_r(json_encode($arr_json));

//echo '<pre>';
//echo json_encode($arr_json);
//echo '</pre>';

?>


