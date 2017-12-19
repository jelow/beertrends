# Make sure the Apt package lists are up to date, so we're downloading versions that exist.
cookbook_file "apt-sources.list" do
  path "/etc/apt/sources.list"
end
execute 'apt_update' do
  command 'apt-get update -y'
end
execute 'apt_upgrade' do
  command 'apt-get upgrade -y'
end

# Base configuration recipe in Chef.
package "wget"
package "ntp"
cookbook_file "ntp.conf" do
  path "/etc/ntp.conf"
end
execute 'ntp_restart' do
  command 'service ntp restart'
end

# Install django dependencies
apt_package 'python3' do
  options '-y'
end
apt_package 'python3-pip' do
  options '-y'
end
apt_package 'python3-venv' do
  options '-y'
end
apt_package 'postgresql' do
  options '-y'
end
apt_package 'postgresql-server-dev-all' do
  options '-y'
end
apt_package 'postgresql-client' do
  options '-y'
end
apt_package 'libpython-dev' do
  options '-y'
end
apt_package 'nginx' do
  options '-y'
end

# Create and set up the postgresql database
bash 'db_config' do
  user 'postgres'
  code <<-EOH
  if psql -lqt | grep -qw beertrends; then
    echo "Database already exists"
  else
    psql -c "CREATE DATABASE beertrends;"
    psql -c "CREATE USER quasimodo WITH PASSWORD 'mmmbeer';"
    psql -c "ALTER ROLE quasimodo SET client_encoding TO 'utf8';"
    psql -c "ALTER ROLE quasimodo SET default_transaction_isolation TO 'read committed';"
    psql -c "ALTER ROLE quasimodo SET timezone TO 'Canada/Pacific';"
    psql -c "GRANT ALL PRIVILEGES ON DATABASE beertrends TO quasimodo;"
  fi
    EOH
end

# Set up python virtual env and install pip packages
execute 'make_virt_dir' do
  user 'ubuntu'
  cwd '/home/ubuntu'
  command 'mkdir -p .virtualenvs'
end
execute 'do_env' do
  user 'ubuntu'
  cwd '/home/ubuntu/.virtualenvs'
  command 'python3 -m venv djangodev'
end
execute 'activate' do
  user 'ubuntu'
  command '. /home/ubuntu/.virtualenvs/djangodev/bin/activate'
end
execute 'requirements_txt' do
  cwd '/home/ubuntu/beertrends'
  command 'pip3 install -r requirements.txt'
end

# Serve the project with gunicorn and nginx on localhost:8000 with 2 workers
execute 'prepare_static_files' do
  cwd '/home/ubuntu/beertrends'
  command 'mkdir -p ../static;mkdir -p log;python3 manage.py collectstatic --noinput'
end
execute 'nginx_conf' do
  cwd '/home/ubuntu/beertrends'
  command 'sudo cp nginx.conf /etc/nginx/conf.d/beertrends.conf;sudo nginx -s reload'
end
execute 'runserver' do
  user 'ubuntu'
  cwd '/home/ubuntu/beertrends'
  command 'gunicorn -w 2 beertrends.wsgi --reload &'
end

#Create and run migrations for models to work properly
execute 'make_migrations' do
  user 'ubuntu'
  cwd '/home/ubuntu/beertrends'
  command 'python3 manage.py makemigrations'
end
execute 'migrate' do
  user 'ubuntu'
  cwd '/home/ubuntu/beertrends'
  command 'python3 manage.py migrate'
end

execute 'seed_database' do
  user 'ubuntu'
  cwd '/home/ubuntu/beertrends'
  command 'python3 manage.py loaddata fixtures/*'
end
