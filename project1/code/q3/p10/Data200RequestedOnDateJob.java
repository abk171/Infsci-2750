import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class Data200RequestedOnDateJob {
    public static class DataOnDateMapper extends Mapper<Object, Text, Text, LongWritable> {
        private Text dateKey = new Text("16/Jan/2022");
        private LongWritable dataSize = new LongWritable();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] parts = line.split(" ");
            if (parts.length > 6 && parts[3].contains("16/Jan/2022") && "200".equals(parts[8])) {
                String byteSizeStr = parts[9];
                if (!"-".equals(byteSizeStr)) {
                    try {
                        long byteSize = Long.parseLong(byteSizeStr);
                        dataSize.set(byteSize);
                        context.write(dateKey, dataSize);
                    } catch (NumberFormatException e) {
                        System.err.println("Error: Unable to parse byte size as a long.");
                    }
                }
            }
        }
    }

    public static class TotalDataOnDateReducer extends Reducer<Text, LongWritable, Text, LongWritable> {
        private LongWritable result = new LongWritable();

        public void reduce(Text key, Iterable<LongWritable> values, Context context) throws IOException, InterruptedException {
            long sum = 0;
            for (LongWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: Data200RequestedOnDateJob <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Data Requested with Status 200 on 16/Jan/2022");
        job.setJarByClass(Data200RequestedOnDateJob.class);
        job.setMapperClass(DataOnDateMapper.class);
        job.setCombinerClass(TotalDataOnDateReducer.class);
        job.setReducerClass(TotalDataOnDateReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(LongWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
