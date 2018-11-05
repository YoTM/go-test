#!/usr/bin/perl

#use 5.20;
use strict;
use warnings;

print "USE the Perl!\n";

# my $data = <STDIN>;


my $lines="";

my $filename = "data.csv";
open(my $fh, '<:encoding(UTF-8)', $filename)
  or die "Could not open file '$filename' $!";

while (my $row = <$fh>) {
  #chomp $row;
  if($row =~ m/^(https?:\/\/)?([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$/i){
        print $row;
        $lines.=$row;

    }else{
            print $row;
            next;
    }

}

#close(filename);

print "done\n";

print $lines;