header = """
|00 @System     &vector $2 &wst      $1 &rst    $1 &eaddr  $2 &ecode  $1 &pad     $1 &r       $2 &g      $2 &b     $2 &debug  $1 &halt $1
|10 @Console    &vector $2 &read     $1 &pad    $5 &write  $1 &error  $1
|20 @Screen     &vector $2 &width    $2 &height $2 &auto   $1 &pad    $1 &x       $2 &y       $2 &addr   $2 &pixel $1 &sprite $1
|30 @Audio0     &vector $2 &position $2 &output $1 &pad    $3 &adsr   $2 &length  $2 &addr    $2 &volume $1 &pitch $1
|40 @Audio1     &vector $2 &position $2 &output $1 &pad    $3 &adsr   $2 &length  $2 &addr    $2 &volume $1 &pitch $1
|50 @Audio2     &vector $2 &position $2 &output $1 &pad    $3 &adsr   $2 &length  $2 &addr    $2 &volume $1 &pitch $1
|60 @Audio3     &vector $2 &position $2 &output $1 &pad    $3 &adsr   $2 &length  $2 &addr    $2 &volume $1 &pitch $1
|80 @Controller &vector $2 &button   $1 &key    $1 &func   $1
|90 @Mouse      &vector $2 &x        $2 &y      $2 &state  $1 &pad    $3 &scrollx $2 &scrolly $2
|a0 @File0      &vector $2 &success  $2 &stat   $2 &delete $1 &append $1 &name    $2 &length  $2 &read   $2 &write $2
|b0 @File1      &vector $2 &success  $2 &stat   $2 &delete $1 &append $1 &name    $2 &length  $2 &read   $2 &write $2
|c0 @DateTime   &year   $2 &month    $1 &day    $1 &hour   $1 &minute $1 &second  $1 &dotw    $1 &doty   $2 &isdst $1

"""

print_short = """
@print-short-decimal ( short* -- )
	#03e8 DIV2k
		DUP ,print-byte-decimal/second JSR
		MUL2 SUB2
	#0064 DIV2k
		DUP ,print-byte-decimal/third JSR
		MUL2 SUB2
	NIP ,print-byte-decimal/second JMP

@print-byte-decimal ( byte -- )
	#64 DIVk DUP #30 ADD .Console/write DEO MUL SUB
	&second
	#0a DIVk DUP #30 ADD .Console/write DEO MUL SUB
	&third
	             #30 ADD .Console/write DEO
	JMP2r
"""