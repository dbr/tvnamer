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
  puts `pylint --reports=n *.py`
end