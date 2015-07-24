<?php
	require("/usr/local/apache2/htdocs/libs/db.inc");
	require("/usr/local/apache2/htdocs/libs/config.inc");
	require("/usr/local/apache2/htdocs/libs/class.phpmailer.php");
	require("/usr/local/apache2/htdocs/libs/class.smtp.php");
	include("/usr/local/apache2/htdocs/cron/valid_email.php");
	mysql_connect('localhost',$db_login,$db_pw) or die ('Could not connect: ' . mysql_error());
	mysql_select_db($db_name) or die('Could not select database');

	date_default_timezone_set("America/Los_Angeles");
	global $To, $Name, $SenderName, $SenderEmail, $today;
	$today = date("Y-m-d");
	echo $today . "\n";

	#SEND EMAIL TO SENDER FOR ALLCARDs

	$q = "SELECT * FROM messages WHERE status = '0' AND facebook_post = '0' AND view_count <= '1'";
	$r = mysql_query($q);
	while($row = mysql_fetch_array($r))
	{
		echo "Fetching data from messages...\n";
		$id = $row['message_id'];
		$SenderName = $row['sender_name'];
		$SenderEmail = $row['sender_email'];
		print $SenderEmail;
		$Hash_tmp = $row['hash'];
		$Hash = preg_replace("/[^\pL\pN\p{Zs}'-]/u", "", $Hash_tmp);
		$To = $row['recipient_email'];
		$Name = $row['recipient_name'];
		$Facebook = $row['facebook_post'];
		$CardId = $row['card_id'];
		$Image = $row['image_name'];
		$SendDate = $row['send_date'];
		sendMailSent($To,$Name,$SenderName,$SenderEmail,$Hash,$id,$Facebook,$Image,$base_url,$SendDate,$today);
	}

	function sendMailSent($To,$Name,$SenderName,$SenderEmail,$Hash,$id,$Facebook,$Image,$base_url,$SendDate,$today)
	{
		if($SendDate == $today) {
			$send_msg = "<p>Your Robert Goulet electronic greeting has been sent to <a class=\"email\" href=\"mailto:$To\">$To</a></p>";
		} else {
			$newDate = date("m-d-Y", strtotime($SendDate)); 
			$send_msg = "<p>Your Robert Goulet electronic greeting has been scheduled to be sent on $newDate to <a class='email' href='mailto:$To'>$To</a></p>";
		}
		# Let's valid the email address first
		$validEmailResult = validEmail($To);
		#echo "validEmailResult = " . $validEmailResult;
		if($validEmailResult == '1') {
			echo "\nValid Email address found: " . $To . " Return Code for valid email is: " . $validEmailResult . "\n";
			echo "Sending ecard sent email to " . $Name . "," . $To . "\n";
			$mail = new PHPMailer();
			$url = "http://www.robertgouletgreetingcards.com/images/emailHeader.jpg"; 
			$urlhash = "http://www.robertgouletgreetingcards.com/index.php?v=view&f=notnew&hash=$Hash";
			$Subject = $SenderName . ", Your Robert Goulet Greeting Card Has Been Sent!";
			$From = "rggc-admin@robertgouletgreetingcards.com";
					
			$mail->IsSMTP();
			$mail->Host = "robertgouletgreetingcards.com";
			$mail->SMTPAuth = false;
			$mail->From = $From;
			$mail->FromName = "Robert Goulet Greeting Cards";
			$mail->AddAddress($SenderEmail);
			$mail->IsHTML(true);
			$mail->Subject = $Subject;
			$mail->Body = "
				<html>
				       <head>
					<style type=\"text/css\">
						body {
							background: #000;
							font-family: serif;
							color: #ffcc00;
						}       
						a.email:link {
							font-size: 12px;
						}
						p {
							text-align: justify;
						}
						a:hover {color:yellow; font-weight:bold}
						a:visited {color:yellow}
						a:active {color:yellow}
						a:link {color:yellow}
					</style>
					</head>
					<body>
					<body bgcolor=\"black\">
					<center>
					<table width=\"1100\">
						<tr>
							<td><img src=\"http://www.robertgouletgreetingcards.com/images/emailHeader.jpg\"></td>
						</tr>
					</table>
					</center>
					<p>Dear $SenderName,</p>
				
					$send_msg
				
					<p>Please go to the Cards History page under Manage Accounts to see the
					status of the cards you have sent.</p>
				
					<p>This card can be viewed by going <a href=\"http://www.robertgouletgreetingcards.com/index.php?v=view&f=notnew&hash=$Hash\">Here</a></p>
				
					<p>With best wishes.</p>
					<p>Robert Goulet Greeting Cards</p>
					<br>
					<br>
					<center>
					<p align=\"left\">&copy; 2011 RGGC/ROGO/ROVE. All rights reserved.</p>
					</center>
					</body>
				</html>
			";
			if(!$mail->Send())
			{
				echo "Message could not be sent. <p>";
				echo "Mailer Error: " . $mail->ErrorInfo;
				exit;
			}
		} else {
			echo "\nEmail address is not valid for: " . $To . " Return Code for valid email is: " . $validEmailResult . "\n";
			sendWarning($SenderEmail,$SenderName,$To);
		}
		
		if($SendDate == $today) {
			$validEmailResult = validEmail($To);
			#echo "validEmailResult = " . $validEmailResult;
			if($validEmailResult == '1') {
				echo "Valid Email address found: " . $To . " Return Code for valid email is: " . $validEmailResult . "\n";
				echo "Sending ecard sent email to " . $Name . "," . $To . "\n";
				echo "Sending ecard to " . $Name . "," . $To . "\n";
				
				$Subject = $Name . ", You have been sent a Robert Goulet Greeting Card!";
				$From = "rggc-admin@robertgouletgreetingcards.com";
				
				$mail = new PHPMailer();
				$mail->IsSMTP();
				$mail->Host = "robertgouletgreetingcards.com";
				$mail->SMTPAuth = false;
				$mail->From = $From;
				$mail->FromName = "Robert Goulet Greeting Cards";
				$mail->AddAddress($To);
				$mail->WordWrap = 200;
				$mail->IsHTML(true);
				$mail->Subject = $Subject;
				$mail->Body = "
					<html>
					       <head>
						<style type='text/css'>
							body {
								background: #000;
								font-family: serif;
								color: #ffcc00;
							}       
							a.email:link {
								font-size: 12px;
							}
							p {
								text-align: justify;
							}
							a:hover {color:yellow; font-weight:bold}
							a:visited {color:yellow}
							a:active {color:yellow}
							a:link {color:yellow}
						</style>
						</head>
						<body>
						<body bgcolor='black'>
						<center>
						<table width='1100'>
							<tr>
								<td><img src='http://www.robertgouletgreetingcards.com/images/emailHeader.jpg'></td>
							</tr>
						</table>
						</center>
						<p>You Have Been Sent a Robert Goulet Greeting Card!</p>
						<br>
						<p>Dear $Name,</p>
		
						<p>$SenderName has sent you a Robert Goulet electronic greeting.</p>
					
						<p>Please click on the following to see your card:<br>		
						<a class='email' href='http://www.robertgouletgreetingcards.com/index.php?v=view&f=new&hash=$Hash'>Pickup My Ecard</a></p>
		
						<p>Alternatively, please visit <a class='email' href='http://www.robertgouletgreetingcards.com'>robertgouletgreetingcards.com</a></p>
						<br>	
						<p>If you're not already a member we hope you will consider joining <a class='email' href='http://www.robertgouletgreetingcards.com/index.php?v=register'>robertgouletgreetingcards.com</a></p>
						<p>Please share our greeting cards with others.</p>
						<br>	
						<p>With best wishes,</p>
						<p>Robert Goulet Greeting Cards</p>
						<br>
						<br>
						<center>
						<p align='left'>&copy; 2011 RGGC/ROGO/ROVE. All rights reserved.</p>
						</center>
						</body>
					</html>
				";
				if(!$mail->Send())
				{
					echo "Message could not be sent. <p>";
					echo "Mailer Error: " . $mail->ErrorInfo;
					exit;
				}
			} else {
				echo "Email address is not valid for: " . $To . " Return Code for valid email is: " . $validEmailResult . "\n";
				#sendWarning($SenderEmail,$SenderName,$To);
			}
		}
		$status = 1;
		chgStatus($id,$status);
	}
	
	$qsend = "SELECT * FROM messages WHERE status = '10' AND send_date = '$today' AND facebook_post = '0' AND view_count <= '1'";
	$rsend = mysql_query($qsend);
	while($row2 = mysql_fetch_array($rsend))
	{
		echo "Fetching data from messages...\n";
		$id = $row2['message_id'];
		$SenderName = $row2['sender_name'];
		$SenderEmail = $row2['sender_email'];
		$Hash_tmp = $row2['hash'];
		$Hash = preg_replace("/[^\pL\pN\p{Zs}'-]/u", "", $Hash_tmp);
		$To = $row2['recipient_email'];
		$Name = $row2['recipient_name'];
		$Facebook = $row2['facebook_post'];
		$CardId = $row2['card_id'];
		$Image = $row2['image_name'];
		$SendDate = $row2['send_date'];
		sendMailScheduled($To,$Name,$SenderName,$SenderEmail,$Hash,$id,$Facebook,$Image,$base_url,$SendDate,$today);
	}
	
	function sendMailScheduled($To,$Name,$SenderName,$SenderEmail,$Hash,$id,$Facebook,$Image,$base_url,$SendDate,$today)
	{		
		if($SendDate == $today) {
			# Let's valid the email address first
			$validEmailResult = validEmail($SenderEmail);
			#echo "validEmailResult = " . $validEmailResult;
			if($validEmailResult == '1') {
				echo "Valid Email address found: " . $SenderEmail . " Return Code for valid email is: " . $validEmailResult . "\n";
				echo "Sending ecard to " . $Name . "," . $To . "\n";
				
				$From = "rggc-admin@robertgouletgreetingcards.com";
				$Subject = $Name . ", You Have Been Sent a Robert Goulet Greeting Card!";
				
				$mail = new PHPMailer();
				$mail->IsSMTP();
				$mail->Host = "robertgouletgreetingcards.com";
				$mail->SMTPAuth = false;
				$mail->From = $From;
				$mail->FromName = "Robert Goulet Greeting Cards";
				$mail->AddAddress($To);
				$mail->WordWrap = 200;
				$mail->IsHTML(true);
				$mail->Subject = $Subject;
				$mail->Body = "
					<html>
					       <head>
						<style type='text/css'>
							body {
								background: #000;
								font-family: serif;
								color: #ffcc00;
							}       
							a.email:link {
								font-size: 12px;
							}
							p {
								text-align: justify;
							}
							a:hover {color:yellow; font-weight:bold}
							a:visited {color:yellow}
							a:active {color:yellow}
							a:link {color:yellow}
						</style>
						</head>
						<body>
						<body bgcolor='black'>
						<center>
						<table width='1100'>
							<tr>
								<td><img src='http://www.robertgouletgreetingcards.com/images/emailHeader.jpg'></td>
							</tr>
						</table>
						</center>
						<p>You Have Been Sent a Robert Goulet Greeting Card!</p>
						<br>
						<p>Dear $Name,</p>
		
						<p>$SenderName has sent you a Robert Goulet electronic greeting.</p>
					
						<p>Please click on the following to see your card:<br>		
						<a class='email' href='http://www.robertgouletgreetingcards.com/index.php?v=view&f=new&hash=$Hash'>Pickup My Ecard</a></p>
		
						<p>Alternatively, please visit <a class='email' href='http://www.robertgouletgreetingcards.com'>robertgouletgreetingcards.com</a></p>
						<br>	
						<p>If you're not already a member we hope you will consider joining <a class='email' href='$base_url/index.php?v=register'>robertgouletgreetingcards.com</a></p>
						<p>Please share our greeting cards with others.</p>
						<br>	
						<p>With best wishes,</p>
						<p>Robert Goulet Greeting Cards</p>
						<br>
						<br>
						<center>
						<p align='left'>&copy; 2011 RGGC/ROGO/ROVE. All rights reserved.</p>
						</center>
						</body>
					</html>
				";
				if(!$mail->Send())
				{
					echo "Message could not be sent. <p>";
					echo "Mailer Error: " . $mail->ErrorInfo;
					exit;
				}
			} else {
				echo "Email address is not valid for: " . $SenderEmail . " Return Code for valid email is: " . $validEmailResult . "\n";
				#sendWarning($SenderEmail,$SenderName,$To);
			}
		}
		$status = 2;
		chgStatus($id,$status);
	}

	#SEND EMAIL TO SENDEE FOR ALL CARDS

	$qview = "SELECT * FROM messages WHERE status = '2' AND facebook_post = '0' AND view_date = '$today' AND view_count <= '1'";
	$rview = mysql_query($qview);
	while($row1 = mysql_fetch_array($rview))
	{
                $id = $row1['message_id'];
                $SenderName = $row1['sender_name'];
		$SenderEmail = $row1['sender_email'];
                $Hash = $row1['hash'];
                #$Code = $row1['rggc_code'];
		$To = $row1['recipient_email'];
		echo $SenderName;
		echo $SenderEmail;
		sendMailView($To,$SenderName,$SenderEmail,$Hash,$id,$base_url);
	}
	
	function sendMailView($To,$SenderName,$SenderEmail,$Hash,$id,$base_url)
	{
		echo "Sending email viewed email to " . $SenderName . "\n";
		
		$Subject = $SenderName . ", Your Robert Goulet Greeting Card Has Been Viewed!";
		$From = "rggc-admin@robertgouletgreetingcards.com";
		
		$mail = new PHPMailer();
		$mail->IsSMTP();
		$mail->Host = "robertgouletgreetingcards.com";
		$mail->SMTPAuth = false;
		$mail->From = $From;
		$mail->FromName = "Robert Goulet Greeting Cards";
		$mail->AddAddress($SenderEmail);
		$mail->WordWrap = 200;
		$mail->IsHTML(true);
		$mail->Subject = $Subject;
		$mail->Body = "
			<html>
				<head>
				<style type='text/css'>
					body {
        					background: #000;
        					font-family: serif;
        					color: #ffcc00;
					}	
					a.email:link {
        					font-size: 12px;
					}
					p {
        					text-align: justify;
					}
					a:hover {color:yellow; font-weight:bold}
					a:visited {color:yellow}
					a:active {color:yellow}
					a:link {color:yellow}
				</style>
				</head>
				<body>
				<body bgcolor='black'>
				<center>
				<table width='1100'>
					<tr>
						<td><img src='http://www.robertgouletgreetingcards.com/images/emailHeader.jpg'></td>
					</tr>
				</table>
				</center>
				<p>Dear $SenderName,</p>
			
				<p>Your Robert Goulet electronic greeting has been viewed by $To.</p>
			
				<p>Please go to the Cards History page under Manage Accounts to see the
				status of the cards you have sent.</p>
			
				<p>With best wishes.</p>
				<p>Robert Goulet Greeting Cards</p>
				<br>
				<br>
				<center>
				<p align='left'>&copy; 2011 RGGC/ROGO/ROVE. All rights reserved.</p>
				</center>
				</body>
			</html>
                ";
		if(!$mail->Send())
		{
			echo "Message could not be sent. <p>";
			echo "Mailer Error: " . $mail->ErrorInfo;
			exit;
		}
		
		$status = 3;
	
		chgStatus($id,$status);
	}

	function chgStatus($id,$status)
	{
		$q1 = "UPDATE messages SET status = '$status' WHERE message_id = $id";
		$r1 = mysql_query($q1);
	}
	
	function sendWarning($SenderEmail,$SenderName,$To)
	{
	
		$mail = new PHPMailer();
		$url = "http://www.robertgouletgreetingcards.com/images/emailHeader.jpg"; 
		#$urlhash = "http://www.robertgouletgreetingcards.com/index.php?v=view&f=notnew&hash=$Hash";
		$Subject = "WARNING - " . $SenderName . ", there was a problem with Your Robert Goulet Greeting Card";
		$From = "rggc-admin@robertgouletgreetingcards.com";
				
		$mail->IsSMTP();
		$mail->Host = "robertgouletgreetingcards.com";
		$mail->SMTPAuth = false;
		$mail->From = $From;
		$mail->FromName = "Robert Goulet Greeting Cards";
		$mail->AddAddress($SenderEmail);
		$mail->IsHTML(true);
		$mail->Subject = $Subject;
		$mail->Body = "
			<html>
			       <head>
				<style type=\"text/css\">
					body {
						background: #000;
						font-family: serif;
						color: #ffcc00;
					}       
					a.email:link {
						font-size: 12px;
					}
					p {
						text-align: justify;
					}
					a:hover {color:yellow; font-weight:bold}
					a:visited {color:yellow}
					a:active {color:yellow}
					a:link {color:yellow}
				</style>
				</head>
				<body>
				<body bgcolor=\"black\">
				<center>
				<table width=\"1100\">
					<tr>
						<td><img src=\"http://www.robertgouletgreetingcards.com/images/emailHeader.jpg\"></td>
					</tr>
				</table>
				</center>
				<p>Dear $SenderName,</p>
			
				<p>There was a problem with the ecard addressed to <b><i>$To</i></b>, it is not a valid email address.</p>
				<p>Unfortunately, we were NOT able to deliver this ecard.</p>
				
				<p>Please correct the email address in your Address Book, then send this ecard again.</p>
			
				<p>With best wishes.</p>
				<p>Robert Goulet Greeting Cards</p>
				<br>
				<br>
				<center>
				<p align=\"left\">&copy; 2011 RGGC/ROGO/ROVE. All rights reserved.</p>
				</center>
				</body>
			</html>
		";
		if(!$mail->Send())
		{
			echo "Message could not be sent. <p>";
			echo "Mailer Error: " . $mail->ErrorInfo;
			exit;
		}		
	}

?>
