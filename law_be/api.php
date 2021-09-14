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
    SELECT AA001,AA002,AA004,AA007,'法規名稱' as SEARCH_TYPE
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
    SELECT DISTINCT AC002,AC003,AC006,AC007,AC008,'法條內容' as SEARCH_TYPE
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
function query_law_aa(){
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



function query_law_ab()
{
    $AA002 = $_GET['AA002'];
    
    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
    
    
    $sql = "
    SELECT AB001,AB002,AB003,AB005,
    CASE WHEN ifnull((select AC005 from LAWAC WHERE AC003=AB002 AND AC004 = AB003 LIMIT 1),0) = 0 
    THEN (select AC005 from LAWAC WHERE AC003=AB002 AND AC004 = (AB003+1) LIMIT 1) else (select AC005 from LAWAC WHERE AC003=AB002 AND AC004 = AB003 LIMIT 1) END AS numStart
    FROM LAWAB    
    WHERE AB002='{$AA002}'
    ORDER BY AB003;";

    $result = $link->query($sql);
    
    $arr_json = array();
    while($row =mysqli_fetch_assoc($result))
    {
        $arr_json[] = $row;
    }

    mysqli_close($link);
    
    echo json_encode($arr_json);
}

function query_law_ab_count(){
    $AA002 = $_GET['AA002'];
    
    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);
    
    
    $sql = "
    SELECT count(AB002) as cnt
    FROM LAWAB    
    WHERE AB002='{$AA002}'
    ORDER BY AB003;";

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
function query_law_ac_all(){
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
function query_law_ac_single(){
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


//LawAll 單身查詢
function query_detail_by_AB003(){
    $AA002 = $_GET['AA002'];
    $AB003 = $_GET['AB003'];
    

    
        
    $link = mysqli_connect(DB_SERVER, DB_USERNAME, DB_PASSWORD, DB_NAME);    
    $where = " ";

    $sql = "
    with tmp_ab as (
        SELECT * FROM LAWAB where AB002='{$AA002}' AND FIND_IN_SET(AB003,get_child_list_ab('{$AB003}','{$AA002}'))
    )
      SELECT '' AS AA003,'' AS AA004
      ,AB002,AB003
      ,AB005
      ,'0' AS AC005
      ,'' AS AC010
      ,'' AS AC011
      FROM LAWAB 
      WHERE AB002='{$AA002}' AND FIND_IN_SET(AB003,get_parent_list_ab('{$AB003}','{$AA002}'))
      UNION ALL
      SELECT AA003,AA004
          ,AB002,AB003
          ,AB005
          ,AC006
          ,AC010
          ,AC011
          FROM LAWAA 
          LEFT JOIN tmp_ab ON AA002 = AB002
          LEFT JOIN LAWAC ON AC003 = AB002 AND AC004 = AB003
          WHERE AA002='{$AA002}' 
          ORDER BY AB003
          ,CAST(SUBSTRING_INDEX(AC005,'-', 1) AS UNSIGNED) ASC
          ,CASE WHEN LOCATE('-',AC005) >0 THEN CAST(SUBSTRING_INDEX(AC005,'-', -1) AS UNSIGNED) ELSE 0 END ASC;
    ";
    //echo $sql;
    //exit;
    $result = $link->query($sql);
    

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
    case 'query_law_aa':
        query_law_aa();
        break;   
    case 'query_law_ab':
        query_law_ab();
        break;         
    case 'query_law_ac_all':
        query_law_ac_all();
        break;
    case 'query_law_ac_single':
        query_law_ac_single();
        break;        
    case 'query_detail_by_AB003':
        query_detail_by_AB003();
        break; 
    case 'query_law_ab_count':
        query_law_ab_count();
        break;         
                
}

// echo $where;
// exit;





//print_r(json_encode($arr_json));

//echo '<pre>';
//echo json_encode($arr_json);
//echo '</pre>';

?>


