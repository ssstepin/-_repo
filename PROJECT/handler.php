<?php
    ini_set('display_errors', 0);
    ini_set('display_startup_errors', 0);
    error_reporting(E_ALL);

    $users_yes_ans = array();
    $users_yes_ans[0] = 45;
    $users_yes_ans[1] = 40;
    $users_yes_ans[2] = 33;
    $users_yes_ans[3] = 32;
    $users_yes_ans[4] = 28;
    $users_yes_ans[5] = 22;
    $users_yes_ans[6] = 20;
    $users_yes_ans[7] = 18;
    $users_yes_ans[8] = 11;
    $users_yes_ans[9] = 5;

    function init_q(){
        require_once 'login.php';
        $connection = new mysqli($hn, $un, $pw, $db);
        if($connection->connect_error) die("Fatall Error");
        $questions = array();
        // $questions[] = "Учился ли ты в 9 классе лицея НИУ ВШЭ?";
        // $questions[] = "Учился ли ты на Факультете дополнительной подготовки (ФДП) в НИУ ВШЭ ?";
        // $questions[] = "Ты учился в своей школе в профильном классе до лицея (математика, физмат или информатика)?";
        // $questions[] = "Твои оценки по алгебре и геометрии за год (за 9 класс) были 5?";
        // $questions[] = "Твоя оценка по информатике за год (за 9 класс) была 5?";
        // $questions[] = "Ты занимался с репетиторами по предмету\предметам, которые нужно было сдавать на экзаменах в лицей?";
        // $questions[] = "Участвовал ли ты в олимпиадах по математике/информатике до поступления в лицей?";
        // $questions[] = "До лицея занимался ли ты в МШП (Московская школа программистов)/Яндекс.Лицее/Tinkoff Generation/на других спецкурсах по программированию?";
        // $questions[] = "Ты решал демоверсии лицейских экзаменов перед вступительными испытаниями?";
        // $questions[] = "Ты собирал информацию об экзаменах и поступлении: в группах лицея и абитуриентов Вконтакте, на сайте НИУ ВШЭ, на форуме лицея, разборы тестов в ютубе и т.д.?";
        $query = "SELECT * FROM questions";
        // $result = $connection->query($query);
        $result = mysqli_query($connection, $query);
        if(!$result) die("Fatal Error");

        while ($r = mysqli_fetch_array($result)) {
            $questions[] = htmlspecialchars("{$r['text']}");
          }

        $result->close();
        $connection->close();
        return $questions;
    }

    $Questions = init_q(); //инициализация вопросов

    function count_pos($answers, $ans_count, $user_answers){ //$answers - сколько "Да" на вопросы (массив), $ans_count - сколько всего ответивших на все вопросы, $user_answers - ответы пользователя: 1 - "Да", 0 - "Нет"
        $sum = 0;
        for($i = 0; $i < count($answers); ++$i){
            if($user_answers[$i] == 1){
                $sum += $answers[$i];
            }
            else{
                $sum += $ans_count - $answers[$i];
            }
        }
        return $sum / (count($answers) * $ans_count);
    }

    function check_all_user_answers($q_count){
        for($i = 0; $i < $q_count; ++$i){
            if(!isset($_POST["q_$i"])){
                return FALSE;
            }
        }
        return TRUE;
    }

    function check_any_user_answers($q_count){
        for($i = 0; $i < $q_count; ++$i){
            if(isset($_POST["q_$i"])){
                return TRUE;
            }
        }
        return FALSE;
    }

    function get_user_answers($q_count){
        $answers = array();
        for($i = 0; $i < $q_count; ++$i){
            if($_POST["q_$i"] == "y"){
                $answers[$i] = 1;
            }
            else{
                $answers[$i] = 0;
            }
        }
        return $answers;
    }

    echo <<<_END
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Form</title>
        <link rel = "stylesheet" href = "style.css">
    </head>
    <body>
        <form method="POST" action = "handler.php">
    _END;
    for ($count = 0; $count < 10; ++$count){
        echo <<<_END
        <div class = "question">
            <label for = "$count">$Questions[$count]</label>
            <div>
                <input id = "q_yes_$count" type = "radio" name = "q_$count" value = "y">
                <label for = "q_yes_$count">Да</label>
            </div>
            <div>
                <input id = "q_no_$count" type = "radio" name = "q_$count" value = "n">
                <label for = "q_no_$count">Нет</label>
            </div>
        </div>
        _END;
    }
    echo <<<_END
        <input type = "submit">
        </form>
    </body>
    </html>
    _END;
    if(!check_any_user_answers(count($Questions))){
        echo "No answers given!";
    }
    else{
        if(!check_all_user_answers(count($Questions))){
            echo "Not enough answers!";
        }
        else{
            $res = count_pos($users_yes_ans, 48, get_user_answers(count($Questions)));
            echo $res." ";
        }
    }
?>