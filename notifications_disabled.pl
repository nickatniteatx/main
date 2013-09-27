#!/usr/bin/perl

use Nagios::StatusLog;
use Getopt::Std;
use Data::Dumper;
use strict;
use warnings;

#Location of nagios.dat
our $opt_l;
getopt('l:');
$opt_l = "/usr/local/nagios/var/status.dat" if ( !$opt_l );

#Nagios Status Log object
my $log = Nagios::StatusLog->new( Filename => $opt_l, Version => 3.0 );

#Check host notifications
foreach my $host ( $log->list_hosts ) {
    my $obj = $log->host($host);
    printf "Notifications disabled for host: %s\n", $obj->host_name if ($obj->notifications_enabled == 0)

}

#Check service notications on per host basis
#Build HoA services hash
my %servicehash;
foreach my $host ( $log->list_hosts ) {
    my @services = ( $log->list_services_on_host($host) );
    $servicehash{$host} = [ @services ] ;
}
#Check invidual services
foreach my $host ( keys %servicehash ) {
    foreach my $service ( @{ $servicehash{$host} } ) {
	my $svc_stat = $log->service($host,$service);
	printf "Notifications disabled for service: \"%s\" on host: %s\n",$service,$host if ($svc_stat->notifications_enabled == 0);     
    }
}
