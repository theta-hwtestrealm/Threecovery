use strict;
use warnings;

my $email = lc($ARGV[0] // "");

if ($email =~ /none/) {exit 10;} #BLOCKED

$email =~ s/^.*?\://;

print $email;
exit 0;