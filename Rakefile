# PyLint messages to disable
pylint_disable = ["R0903", "C0103", "R0903"]
task :default => [:pep8, :pylint]

def title(text)
  padding = "#" * (79 - (text.length + 1))
  puts "#{padding} #{text}"
end

task :pep8 do
  title("pep8.py")
  puts `python tools/pep8.py *.py`
end

task :pylint do
  title("PyLint")
  puts `pylint --reports=n --disable-msg=#{pylint_disable.join(",")} *.py`
end