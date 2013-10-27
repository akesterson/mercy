class mercy(
  $environment,
  $version,
  $ensure,
  $rabbitmq_uri,
  $process_user    => 'mercy',
  $process_group   => 'mercy',
  $process_threads => 5,
  $servername      => $::fqdn,
  $rabbitmq_user   => 'mercy',
  $rabbitmq_pw     => 'mercy',
  $rabbitmq_vhost  => 'mercy',
  $vhost_dir       => '/etc/apache/httpd/conf.d',
  $apache_service  => 'httpd',
  $port            => 443,
  $postgres_uri    => 'localhost',
  $postgres_user   => 'mercy',
  $postgres_pw     => 'mercy',
  $postgres_db     => 'mercy')
{
             include 'mercy::params'
}
