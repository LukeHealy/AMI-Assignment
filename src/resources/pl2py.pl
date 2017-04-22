#!perl -w

=head1 NAME
pl2py.pl
=head1 DESCRIPTION
Attempts to convert perl scripts to python with the awesome power of regular expressions.
=head1 BUGS
This will (probably) not actually produce runnable python files. But it saves a lot of work converting some perl to python.
More useful if your perl code is well-indented to start with (consider using a source formatter first).
=head1 AUTHOR
Daniel Perrett C<< dperrett@cambridge.org >>
=cut

my $state;
while (my $sLine = <>)
{
    $sLine =~ tr/$//d;
    $sLine =~ s/(?!<\d)\.(?!\d)/+/g;
    $sLine =~ s/::/./g;
    if ($state->{'pod'})
    {
        $sLine =~ s/^=(?!cut)//g;
    }
    elsif ($sLine =~ s/^=(?!cut)/"""/)
    {
        $state->{'pod'} = 1;
    }
    if ($sLine =~ s/^=cut/"""/)
    {
        $state->{'pod'} = 0;
    }
    $sLine =~ s/^\s*package (.*?);/class $1:/g;
    $sLine =~ s/^\s*use /import /g;
    $sLine =~ s/^\bundef\b/None/g;
    $sLine =~ s/^\beq\b/==/g;
    $sLine =~ s/^\bge\b/>=/g;
    $sLine =~ s/^\ble\b/=</g;
    $sLine =~ s/^\bne\b/!=/g;
    $sLine =~ s/^\bgt\b/>/g;
    $sLine =~ s/^\blt\b/</g;
    $sLine =~ s/^\|\|/or/g;
    $sLine =~ s/^&&/and/g;
    $sLine =~ s/\s+{(['"])(.*)\1}/.$2/g;
    #$sLine =~ s/^\s*sub\s*([\w]+)\s*(?:\(([^)]+)\))\s*\{?/def $1 ($2):/g;
    $sLine =~ s/\bsub ([\w]+)(?:\(([^)]+)\))?\s*\{?/def $1:/g;
    $sLine =~ s/\bmy ([\w]+)\s*=/$1 =/g;
    $sLine =~ s/\bmy ([\w]+);//g;
    $sLine =~ s/!/ not /g;
    $sLine =~ s/->\{/./g;
    $sLine =~ s/->\[/./g;
    $sLine =~ s/->/./g;
    $sLine =~ s/\{$/:/g;
    $sLine =~ s/\}//g;
    $sLine =~ s/;$//g;
    print STDOUT $sLine;
}