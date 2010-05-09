# PyLint/PEP8 messages to disable
pylint_disable = ["R0903", "C0103", "R0903", "F0401", "C0301"].join(",")
pep8_disable = ["E501"].join(",")

task :default => [:pep8, :pyflakes, :test]

# Displays a the width of standard terminal, with text at end
def title(text)
  padding = "#" * (79 - (text.length + 1))
  puts "#{padding} #{text}"
end

desc "Removes .pyc files"
task :clean do
  `rm *.pyc`
  `rm */*.pyc`
end

desc "Checks code for PEP8 compliance"
task :pep8 do
  title("pep8.py")
  puts `python tools/pep8.py --ignore=#{pep8_disable} --repeat *.py tests/*.py`
end

desc "Lints the code with PyFlakes"
task :pyflakes do
  title("PyFlake")
  puts `pyflakes .`
end

desc "Lints code with PyLint"
task :pylint do
  title("PyLint")
  puts `pylint --reports=n --disable-msg=#{pylint_disable} tvnamer/*.py tests/*.py`
end

desc "Runs unit tests using nosetests"
task :test do
  title("Unit tests")
  puts `nosetests`
end

desc "Upload current version to PyPi"
task :topypi => :test do
  cur_file = File.open("tvnamer/__init__.py").read()
  tvnamer_version = cur_file.scan(/__version__ = \((.*)\)/)
  tvnamer_version = tvnamer_version[0][0].to_f

  puts "Build sdist and send tvnamer v#{tvnamer_version} to PyPi?"
  if $stdin.gets.chomp == "y"
    puts "Sending source-dist (sdist) to PyPi"

    if system("python setup.py sdist register upload")
      print "tvnamer uploaded!"
    end

  else
    puts "Cancelled"
  end
end
