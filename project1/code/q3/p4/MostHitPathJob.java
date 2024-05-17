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
import java.util.HashMap;
import java.util.Map;

public class MostHitPathJob {
    public static class PathMapper extends Mapper<Object, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
    
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] parts = line.split("\"");
            if (parts.length > 1) {
                String[] requestParts = parts[1].split(" ");
                if (requestParts.length > 1) {
                    context.write(new Text(requestParts[1]), one);
                }
            }
        }
    }
    
    public static class MaxHitPathReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private Map<Text, IntWritable> countMap = new HashMap<>();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            countMap.put(new Text(key), new IntWritable(sum));
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            Map.Entry<Text, IntWritable> maxEntry = null;
            for (Map.Entry<Text, IntWritable> entry : countMap.entrySet()) {
                if (maxEntry == null || entry.getValue().get() > maxEntry.getValue().get()) {
                    maxEntry = entry;
                }
            }
            if (maxEntry != null) {
                context.write(maxEntry.getKey(), maxEntry.getValue());
            }
        }
    }

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: MostHitPathJob <input path> <output path>");
            System.exit(-1);
        }

        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "Most Hit Path");
        job.setJarByClass(MostHitPathJob.class);
        job.setMapperClass(PathMapper.class);
        job.setReducerClass(MaxHitPathReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
