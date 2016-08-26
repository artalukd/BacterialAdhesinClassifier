#!usr/bin/perl -w
use strict;
use warnings;
my $filename = '';
my $fileout = '';
my @arr = ();
my %hash = ();
my $file = '';
my $giseq = '';
my $seq = '';
my @t = ();
my $d = 1;
my $i = 0;
my $j =0;
my $x = '';

my @a = qw(A C D E F G H I K L M N P Q R S T V W Y);
my @b = qw(A C D E F G H I K L M N P Q R S T V W Y);

for($i=0;$i<20;$i++)
{
	for($j=0;$j<20;$j++)
	{  
		$x = $a[$i].$b[$j];
 		push (@t,$x);
  	}
}

foreach my $c(@t)
{
	$hash{$c} = $d;
	$d++;
}

print "Enter your inputfile in fasta format\n";
$filename =<STDIN>;
chomp $filename;
print "Enter your outputfile\n";
$fileout =<STDIN>;
chomp $fileout;
open(FH,"<$filename") or die "failed to open file because of $!";
@arr = <FH>;
close FH;
$file = join('',@arr);
@arr = ();
open(FO,">$fileout") or die "failed to open file because of $!";

while($file =~ /^>.*\n(^(?!>).*\n)+/gm)
{
      	my $p=0;
      	my @q=();
      	my @seqarr= ();
      	my $header = '';
      	my $id = '';
      	
      	$giseq = $&;
 	$giseq =~ s/\*//gm;
       	$giseq =~ /^>(.*\n)/;
       	$seq = $';
       	$header = $&;
       	$header =~ s/\n//g;
	
       	        $seq =~ s/\s//gm;
       		$seq =~ s/\n//gm;
       	
       	if($seq =~ /B|J|O|U|X|Z/)
	{
        	next;
      	}
	else
        {print FO "$giseq";}	
  	
}
close FO;
exit;

