import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;

public class DataRequestedOnDateJob {
    public static class DataRequestedMapper extends Mapper<Object, Text, Text, IntWritable> {

        private Text dateKey = new Text("19/Dec/2020");
        private IntWritable dataSize = new IntWritable();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String[] parts = value.toString().split(" ");
            if (parts.length > 6 && parts[3].contains(dateKey.toString())) {
                String byteSize = parts[9];
                if (!"-".equals(byteSize)) {
                    dataSize.set(Integer.parseInt(byteSize));
                    context.write(dateKey, dataSize);
                }
            }
        }
    }

    public static class TotalDataSizeReducer extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: DataRequestedOnDateJob <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Data Requested on 19/Dec/2020");
        job.setJarByClass(DataRequestedOnDateJob.class);
        job.setMapperClass(DataRequestedMapper.class);
        job.setCombinerClass(TotalDataSizeReducer.class);
        job.setReducerClass(TotalDataSizeReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
