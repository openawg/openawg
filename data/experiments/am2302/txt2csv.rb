require 'json'
require 'date'

# This script converts the JSON log format to a CSV for
# importing to spreadshits.

puts 'temperature,humidity,timestamp,date'
ARGF.each_line do |line|
  data = JSON.parse(line)
  # puts "#{data[0]['value']},#{data[1]['value']},#{Time.at(data[0]['time'],'%Y.%m.%d.%H.%M.%S')}"
  puts "#{data[0]['value']},#{data[1]['value']},#{data[0]['time']},#{Time.at(data[0]['time'])}"
end
