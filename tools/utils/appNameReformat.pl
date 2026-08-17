use strict;
use warnings;

my $text = $ARGV[0] // "";
my $original = $text;

my %replacements = ( #LOWERCASE INPUT ONLY
    'ialiexpress'  => 'Aliexpress',
    'facebook talk' => 'Facebook Messenger Kids',
    'facebook orca' => 'Facebook Messenger',
    'facebook katana' => 'Facebook',
    'googlemobile' => 'Google',
    'google ios youtube' => 'Youtube',
    'google ios ytcreator' => 'Youtube Create',
    'burbn instagram' => 'Instagram',
    'amazon aiv aivapp' => 'Amazon Prime Video', #amazon instant video
    'lemon lvoverseas' => 'CapCut'
);
my $pattern = join '|', map { quotemeta } keys %replacements;

#feel free to add changes to the above code
#i prefer future edits not to be made below as it will inherintly cause issues with the above code

if ($text =~ /com\.apple\./) {exit 10;} #BLOCKED

$text =~ s/^.*?com\.//i;
$text =~ s/\.app$//;
$text =~ s/\b([a-z])/\U$1/g;

$text =~ s/\./ /g;
$text =~ s/^([^\s]+?)(?:app)? \1/$1/i;

$text =~ s/ ios/ iOS/i;

$text =~ s/($pattern)/$replacements{lc($1)}/gi;

if ($text eq "") {
    print "[Bug]: $original became empty";
}
else {
    print $text;
}

exit 0;